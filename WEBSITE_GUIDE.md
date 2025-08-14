# Website Management Guide

## 🏗️ Website Structure

This is a **Jekyll-based static website** that automatically builds and deploys to GitHub Pages. Here's how it's organized:

### 📁 Key Directories
- **`_posts/`** - All your blog posts go here
- **`_layouts/`** - HTML templates for different page types
- **`_includes/`** - Reusable HTML components
- **`_sass/`** - SCSS styling files
- **`assets/`** - Images, CSS, JavaScript, and other static files
- **`_data/`** - Configuration data (menus, etc.)

### 📄 Key Files
- **`_config.yml`** - Main website configuration
- **`index.md`** - Homepage content
- **`about.md`** - About page
- **`404.md` - Custom 404 error page

## ✍️ Adding Blog Posts

### Method 1: Manual Creation (Recommended for beginners)

1. **Create a new folder** in `_posts/` with a descriptive name:
   ```
   _posts/my-new-blog-post/
   ```

2. **Create the markdown file** with the correct naming convention:
   ```
   _posts/my-new-blog-post/2024-01-15-my-new-blog-post.md
   ```
   
   **Naming convention**: `YYYY-MM-DD-title-with-hyphens.md`

3. **Add front matter** at the top of your markdown file:
   ```markdown
   ---
   layout: post
   title: "My New Blog Post Title"
   date: 2024-01-15
   tags: [tag1, tag2, tag3]
   description: "Brief description of your post"
   ---
   ```

4. **Write your content** below the front matter using standard Markdown

### Method 2: Using Jekyll Compose (Advanced)

If you have Jekyll installed locally:
```bash
bundle exec jekyll post "My New Post Title"
```

## 🎨 Front Matter Options

### Required Fields
- **`layout`**: Usually `post` for blog posts
- **`title`**: Your post title
- **`date`**: Publication date (YYYY-MM-DD format)

### Optional Fields
- **`tags`**: Array of tags for categorization
- **`description`**: Brief description for SEO and social sharing
- **`image`**: Featured image path
- **`comments`**: Set to `false` to disable comments
- **`usemathjax`**: Set to `true` if using mathematical equations

## 🖼️ Adding Images to Posts

1. **Place images** in your post's folder:
   ```
   _posts/my-post/
   ├── 2024-01-15-my-post.md
   ├── image1.jpg
   └── image2.png
   ```

2. **Reference them** in your markdown:
   ```markdown
   ![Alt text](image1.jpg)
   ![Alt text](image2.png)
   ```

## 🚀 Workflow: Adding a New Post

### Step 1: Create Your Post
```bash
# Navigate to posts directory
cd _posts

# Create new post folder
mkdir my-new-post

# Create the markdown file
touch my-new-post/2024-01-15-my-new-post.md
```

### Step 2: Write Your Content
Edit the markdown file with your content and proper front matter.

### Step 3: Test Locally (Optional)
```bash
# Install dependencies
bundle install

# Start local server
bundle exec jekyll serve

# Visit http://localhost:4000 to preview
```

### Step 4: Commit and Push
```bash
# Add your new post
git add _posts/my-new-post/

# Commit with descriptive message
git commit -m "Add new blog post: My New Post Title"

# Push to GitHub (triggers automatic deployment)
git push origin master
```

## ⚙️ Configuration Changes

### Site Settings (`_config.yml`)
- **`title`**: Website title
- **`description`**: Site description
- **`timezone`**: Your timezone (currently EST)
- **`url`**: Your domain (currently https://sfwani.github.io)
- **`mode`**: Default theme (currently light)

### Profile Settings
- **`author.name`**: Your name
- **`author.bio`**: Your bio
- **`author.github`**: GitHub username
- **`author.email`**: Your email

## 🔧 Customization

### Styling
- **Main styles**: `_sass/main.scss`
- **Theme-specific**: `_sass/klise/`
- **Custom CSS**: `assets/css/style.scss`

### Layouts
- **Post layout**: `_layouts/post.html`
- **Page layout**: `_layouts/page.html`
- **Home layout**: `_layouts/home.html`

### Navigation
- **Menu items**: `_data/menus.yml`
- **Navigation component**: `_includes/navigation.html`

## 📱 Adding Pages

1. **Create a new markdown file** in the root directory
2. **Add front matter**:
   ```markdown
   ---
   layout: page
   title: "Page Title"
   ---
   ```
3. **Add to navigation** in `_data/menus.yml`

## 🚨 Important Notes

### File Naming
- **Use hyphens, not spaces** in filenames
- **Dates must be in YYYY-MM-DD format**
- **Post titles should be descriptive**

### Git Workflow
- **Always commit with descriptive messages**
- **Push to master branch** to trigger deployment
- **GitHub Actions will automatically build and deploy**

### Content Guidelines
- **Use Markdown syntax** for formatting
- **Keep images optimized** (compress before uploading)
- **Use descriptive alt text** for accessibility

## 🆘 Troubleshooting

### Common Issues
1. **Post not showing**: Check front matter syntax and date format
2. **Images not loading**: Verify file paths and image names
3. **Build errors**: Check for syntax errors in markdown or YAML

### Getting Help
- **Jekyll documentation**: https://jekyllrb.com/docs/
- **Markdown guide**: https://www.markdownguide.org/
- **GitHub Pages**: https://pages.github.com/

## 📚 Quick Reference

### Essential Commands
```bash
# Add new post
git add _posts/new-post/
git commit -m "Add new post: Title"
git push origin master

# Update configuration
git add _config.yml
git commit -m "Update site configuration"
git push origin master

# Check status
git status
git log --oneline
```

### File Structure Template
```
_posts/
├── post-title-1/
│   ├── 2024-01-15-post-title-1.md
│   ├── image1.jpg
│   └── image2.png
└── post-title-2/
    └── 2024-01-16-post-title-2.md
```

---

**Remember**: Every time you push to the `master` branch, GitHub will automatically build and deploy your website to https://sfwani.github.io
