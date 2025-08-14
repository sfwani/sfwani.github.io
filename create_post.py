#!/usr/bin/env python3
"""
Blog Post Creator Script for Jekyll Website
Automates the creation of new blog posts with proper structure and front matter.
"""

import os
import re
from datetime import datetime
import sys

def sanitize_filename(title):
    """Convert title to a safe filename with hyphens."""
    # Remove special characters and replace spaces with hyphens
    filename = re.sub(r'[^\w\s-]', '', title.lower())
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.strip('-')

def get_user_input():
    """Get post details from user input."""
    print("🎯 Blog Post Creator")
    print("=" * 50)
    
    # Get post title
    while True:
        title = input("📝 Post title: ").strip()
        if title:
            break
        print("❌ Title cannot be empty. Please try again.")
    
    # Get date (with default to today)
    today = datetime.now().strftime("%Y-%m-%d")
    while True:
        date_input = input(f"📅 Date (YYYY-MM-DD) [default: {today}]: ").strip()
        if not date_input:
            date_input = today
            break
        
        # Validate date format
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD format.")
    
    # Get tags
    tags_input = input("🏷️  Tags (comma-separated, optional): ").strip()
    tags = []
    if tags_input:
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
    
    # Get description
    description = input("📖 Description (optional): ").strip()
    
    # Get layout (with default)
    layout = input("📋 Layout [default: post]: ").strip() or "post"
    
    return {
        'title': title,
        'date': date_input,
        'tags': tags,
        'description': description,
        'layout': layout
    }

def create_post_structure(post_info):
    """Create the post folder and markdown file."""
    # Create sanitized folder name
    folder_name = sanitize_filename(post_info['title'])
    post_dir = os.path.join('_posts', folder_name)
    
    # Create post directory
    try:
        os.makedirs(post_dir, exist_ok=True)
        print(f"✅ Created directory: {post_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return False
    
    # Create markdown file
    filename = f"{post_info['date']}-{folder_name}.md"
    filepath = os.path.join(post_dir, filename)
    
    # Generate front matter
    front_matter = generate_front_matter(post_info)
    
    # Write the file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(front_matter)
        print(f"✅ Created post file: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error creating file: {e}")
        return False

def generate_front_matter(post_info):
    """Generate the front matter for the post."""
    front_matter = "---\n"
    front_matter += f"layout: {post_info['layout']}\n"
    front_matter += f"title: \"{post_info['title']}\"\n"
    front_matter += f"date: {post_info['date']}\n"
    
    if post_info['tags']:
        tags_str = "[" + ", ".join([f'"{tag}"' for tag in post_info['tags']]) + "]"
        front_matter += f"tags: {tags_str}\n"
    
    if post_info['description']:
        front_matter += f"description: \"{post_info['description']}\"\n"
    
    front_matter += "comments: false\n"
    front_matter += "---\n\n"
    
    # Add some helpful content structure
    front_matter += f"# {post_info['title']}\n\n"
    front_matter += "<!-- Add your content here -->\n\n"
    front_matter += "## Introduction\n\n"
    front_matter += "<!-- Write your introduction here -->\n\n"
    front_matter += "## Main Content\n\n"
    front_matter += "<!-- Write your main content here -->\n\n"
    front_matter += "## Conclusion\n\n"
    front_matter += "<!-- Write your conclusion here -->\n\n"
    
    return front_matter

def show_next_steps(post_info):
    """Show the user what to do next."""
    folder_name = sanitize_filename(post_info['title'])
    filename = f"{post_info['date']}-{folder_name}.md"
    
    print("\n🎉 Post created successfully!")
    print("=" * 50)
    print(f"📁 Post location: _posts/{folder_name}/{filename}")
    print(f"📝 Edit the file to add your content")
    print(f"🖼️  Add images to the _posts/{folder_name}/ folder")
    print("\n🚀 To publish your post:")
    print("   1. Edit the markdown file with your content")
    print("   2. Add any images to the post folder")
    print("   3. Run: git add _posts/{folder_name}/")
    print("   4. Run: git commit -m \"Add new post: {post_info['title']}\"")
    print("   5. Run: git push origin master")
    print("\n💡 Tip: You can now open the markdown file in your editor!")

def main():
    """Main function to run the script."""
    # Check if we're in the right directory
    if not os.path.exists('_posts'):
        print("❌ Error: '_posts' directory not found!")
        print("   Please run this script from your Jekyll website root directory.")
        sys.exit(1)
    
    try:
        # Get user input
        post_info = get_user_input()
        
        # Create the post structure
        if create_post_structure(post_info):
            # Show next steps
            show_next_steps(post_info)
        else:
            print("❌ Failed to create post. Please check the errors above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n❌ Post creation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
