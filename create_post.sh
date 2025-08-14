#!/bin/bash

# Blog Post Creator Script for Jekyll Website
# Simple bash version for creating new blog posts

echo "🎯 Blog Post Creator (Bash Version)"
echo "=================================="

# Check if we're in the right directory
if [ ! -d "_posts" ]; then
    echo "❌ Error: '_posts' directory not found!"
    echo "   Please run this script from your Jekyll website root directory."
    exit 1
fi

# Get post title
while true; do
    read -p "📝 Post title: " title
    if [ -n "$title" ]; then
        break
    fi
    echo "❌ Title cannot be empty. Please try again."
done

# Get date (with default to today)
today=$(date +%Y-%m-%d)
read -p "📅 Date (YYYY-MM-DD) [default: $today]: " date_input
if [ -z "$date_input" ]; then
    date_input=$today
fi

# Validate date format
if ! date -d "$date_input" >/dev/null 2>&1; then
    echo "❌ Invalid date format. Please use YYYY-MM-DD format."
    exit 1
fi

# Get tags
read -p "🏷️  Tags (comma-separated, optional): " tags_input

# Get description
read -p "📖 Description (optional): " description

# Get layout (with default)
read -p "📋 Layout [default: post]: " layout
if [ -z "$layout" ]; then
    layout="post"
fi

# Create sanitized folder name
folder_name=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]/-/g' | sed 's/-\+/-/g' | sed 's/^-\|-$//g')

# Create post directory
post_dir="_posts/$folder_name"
mkdir -p "$post_dir"
echo "✅ Created directory: $post_dir"

# Create markdown file
filename="$date_input-$folder_name.md"
filepath="$post_dir/$filename"

# Generate front matter
cat > "$filepath" << EOF
---
layout: $layout
title: "$title"
date: $date_input
EOF

# Add tags if provided
if [ -n "$tags_input" ]; then
    # Convert comma-separated tags to array format
    tags_array=$(echo "$tags_input" | sed 's/,/", "/g' | sed 's/^/["/; s/$/"]/')
    echo "tags: $tags_array" >> "$filepath"
fi

# Add description if provided
if [ -n "$description" ]; then
    echo "description: \"$description\"" >> "$filepath"
fi

# Complete front matter and add content structure
cat >> "$filepath" << EOF
comments: false
---

# $title

<!-- Add your content here -->

## Introduction

<!-- Write your introduction here -->

## Main Content

<!-- Write your main content here -->

## Conclusion

<!-- Write your conclusion here -->
EOF

echo "✅ Created post file: $filepath"

echo ""
echo "🎉 Post created successfully!"
echo "=================================="
echo "📁 Post location: $post_dir/$filename"
echo "📝 Edit the file to add your content"
echo "🖼️  Add images to the $post_dir folder"
echo ""
echo "🚀 To publish your post:"
echo "   1. Edit the markdown file with your content"
echo "   2. Add any images to the post folder"
echo "   3. Run: git add $post_dir/"
echo "   4. Run: git commit -m \"Add new post: $title\""
echo "   5. Run: git push origin master"
echo ""
echo "💡 Tip: You can now open the markdown file in your editor!"
