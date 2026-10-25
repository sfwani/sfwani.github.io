## Summary

Portainer lets administrators disable bind mounts for regular users through the `AllowBindMountsForRegularUsers` endpoint security setting. The container creation proxy enforces that setting, but it only understands one of the two ways Docker can create a bind mount. A regular user can smuggle a host bind mount past the check by describing it as a `Type: "volume"` mount whose local driver config requests `type=bind`, mounting any path from the Docker host into their container. This is the same class of bypass that was fixed for Swarm services but never carried over to plain container creation.

## Where it lives

The container creation decorator parses an intentionally narrow view of the request body. In `api/http/proxy/factory/docker/containers.go`, the `Mounts` entries are reduced to a single field:

<!-- bug: Type string `json:"Type"` :: mounts are parsed down to the Type field only -->
```go
Mounts      []struct {
    Type string `json:"Type"`
} `json:"Mounts"`
```

and the enforcement loop only rejects the mount when that field is the literal string `bind`:

<!-- bug: if mount.Type == "bind" { :: only rejects mounts literally typed bind -->
```go
if !securitySettings.AllowBindMountsForRegularUsers && len(partialContainer.HostConfig.Mounts) > 0 {
    for _, mount := range partialContainer.HostConfig.Mounts {
        if mount.Type == "bind" {
            return forbiddenResponse, ErrBindMountsForbidden
```

`VolumeOptions.DriverConfig.Options` is never parsed, so a mount declared as `Type: "volume"` sails through. The sibling code for Swarm services, in `api/http/proxy/factory/docker/services.go`, already knows about this trick. Its `partialServiceSpec` parses the nested struct and checks it explicitly:

```go
VolumeOptions *struct {
    DriverConfig *struct {
        Options map[string]string `json:"Options"`
    } `json:"DriverConfig"`
} `json:"VolumeOptions"`
...
if mount.VolumeOptions != nil && mount.VolumeOptions.DriverConfig != nil {
    if mount.VolumeOptions.DriverConfig.Options["type"] == "bind" {
```

The fix existed in one path and was simply absent in the other.

## Impact

A regular Portainer user with endpoint access, on an endpoint where bind mounts are supposed to be forbidden, posts a container create request whose mount is `Type: "volume"` with `DriverConfig.Options` of `type=bind`, `device=/`, `o=bind`. Docker's local volume driver turns that into a bind mount of the host root into the container. I confirmed this against v2.42.0: a container reading `/hostroot/etc/shadow` returned the real host file.

```
root:*:20535:0:99999:7:::
daemon:*:20535:0:99999:7:::
bin:*:20535:0:99999:7:::
```

From there the user has full read and write access to the host filesystem, including `/root/.ssh`, the Docker socket, and everything else, which is a complete escape of the restriction and of the container boundary. The affected range covers `>= 2.33.0` through `2.42.0`, every then current release.

## Fix

Teach the container path the same thing the service path already knows. Extend the `Mounts` struct with the `VolumeOptions.DriverConfig.Options` map and reject any mount whose `Options["type"]` is `bind`, in addition to the existing `Type == "bind"` check. The same validation belongs in the Docker Compose stack path so stacks cannot reintroduce the bypass.
