#!/usr/bin/env python3
"""
Jekyll Post Generator - Enhanced Version with Jinja2 Templates
Generates Jekyll-compatible markdown posts with front matter using Jinja2 templating.
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Dependency validator utility
class DependencyValidator:
    """Validates and manages script dependencies."""
    
    REQUIRED_PACKAGES = {
        'slugify': {
            'module': 'slugify',
            'package': 'python-slugify',
            'description': 'URL slug generation'
        },
        'jinja2': {
            'module': 'jinja2',
            'package': 'Jinja2',
            'description': 'Template engine for YAML formatting'
        },
        'tzdata': {
            'module': 'tzdata',
            'package': 'tzdata',
            'description': 'Timezone database'
        }
    }
    
    @classmethod
    def validate_dependencies(cls) -> None:
        """Validate all required dependencies are installed."""
        missing_deps = []
        
        for dep_name, dep_info in cls.REQUIRED_PACKAGES.items():
            try:
                __import__(dep_info['module'])
            except ImportError:
                missing_deps.append(dep_info)
        
        if missing_deps:
            print("❌ Missing required dependencies:")
            for dep in missing_deps:
                print(f"   • {dep['package']} - {dep['description']}")
            print("\n🔧 Install missing packages using:")
            packages = [dep['package'] for dep in missing_deps]
            print(f"   pip install {' '.join(packages)}")
            sys.exit(1)

# Validate dependencies before importing
DependencyValidator.validate_dependencies()

from slugify import slugify
from jinja2 import Environment, BaseLoader, TemplateError


class PostGeneratorError(Exception):
    """Custom exception for post generation errors."""
    pass


class InputValidator:
    """Validates and sanitizes user inputs."""
    
    @staticmethod
    def validate_title(title: str) -> str:
        """Validate and sanitize post title."""
        if not title or not title.strip():
            raise PostGeneratorError("Post title cannot be empty")
        
        title = title.strip()
        if len(title) > 200:
            raise PostGeneratorError("Post title cannot exceed 200 characters")
        
        # Check for problematic characters
        forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(char in title for char in forbidden_chars):
            raise PostGeneratorError(f"Title contains forbidden characters: {', '.join(forbidden_chars)}")
        
        return title
    
    @staticmethod
    def validate_category(category: str, category_type: str = "category") -> str:
        """Validate category inputs."""
        if not category or not category.strip():
            raise PostGeneratorError(f"{category_type.capitalize()} cannot be empty")
        
        category = category.strip()
        if len(category) > 50:
            raise PostGeneratorError(f"{category_type.capitalize()} cannot exceed 50 characters")
        
        # Only allow alphanumeric, spaces, hyphens, and underscores
        if not all(c.isalnum() or c in ' -_' for c in category):
            raise PostGeneratorError(f"{category_type.capitalize()} can only contain letters, numbers, spaces, hyphens, and underscores")
        
        return category
    
    @staticmethod
    def validate_tags(tags_input: str) -> List[str]:
        """Validate and parse tags."""
        if not tags_input or not tags_input.strip():
            raise PostGeneratorError("At least one tag is required")
        
        tags = [tag.strip().lower() for tag in tags_input.split(',')]
        valid_tags = []
        
        for tag in tags:
            if not tag:
                continue
            
            if len(tag) > 30:
                raise PostGeneratorError(f"Tag '{tag}' exceeds 30 character limit")
            
            if not all(c.isalnum() or c in '-_' for c in tag):
                raise PostGeneratorError(f"Tag '{tag}' can only contain letters, numbers, hyphens, and underscores")
            
            valid_tags.append(tag)
        
        if not valid_tags:
            raise PostGeneratorError("No valid tags provided")
        
        if len(valid_tags) > 10:
            raise PostGeneratorError("Maximum 10 tags allowed")
        
        return valid_tags
    
    @staticmethod
    def validate_date(date_str: str) -> datetime:
        """Validate custom date input."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise PostGeneratorError("Date must be in YYYY-MM-DD format (e.g., 2023-12-25)")
    
    @staticmethod
    def validate_author(author: str) -> str:
        """Validate author input."""
        if not author or not author.strip():
            return ""
        
        author = author.strip()
        if len(author) > 100:
            raise PostGeneratorError("Author name cannot exceed 100 characters")
        
        return author
    
    @staticmethod
    def validate_description(description: str) -> str:
        """Validate description input."""
        if not description or not description.strip():
            return ""
        
        description = description.strip()
        if len(description) > 500:
            raise PostGeneratorError("Description cannot exceed 500 characters")
        
        return description


class JekyllTemplateEngine:
    """Handles Jinja2 template rendering for Jekyll posts."""
    
    DEFAULT_TEMPLATE = """---
title: {{ title }}
date: {{ date }}
categories: [{{ categories|join(', ') }}]
tags: {{ tags }}
{%- if author %}
author: {{ author }}
{%- endif %}
{%- if description %}
description: {{ description }}
{%- endif %}
{%- if custom_fields %}
{%- for key, value in custom_fields.items() %}
{{ key }}: {{ value }}
{%- endfor %}
{%- endif %}
---

<!-- Write your post content here -->

"""
    
    def __init__(self, custom_template: Optional[str] = None):
        """Initialize the template engine."""
        self.env = Environment(loader=BaseLoader())
        self.template_content = custom_template or self.DEFAULT_TEMPLATE
    
    def render_post(self, **kwargs) -> str:
        """Render the post using Jinja2 template."""
        try:
            template = self.env.from_string(self.template_content)
            return template.render(**kwargs)
        except TemplateError as e:
            raise PostGeneratorError(f"Template rendering failed: {e}")


class PostGenerator:
    """Generates Jekyll posts with proper front matter using Jinja2 templates."""
    
    DEFAULT_TIMEZONE = "Asia/Kolkata"
    DEFAULT_OUTPUT_DIR = "_posts"
    
    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR, 
                 timezone: str = DEFAULT_TIMEZONE,
                 custom_template: Optional[str] = None):
        """
        Initialize the PostGenerator.
        
        Args:
            output_dir: Directory where posts will be saved
            timezone: Timezone for post timestamps
            custom_template: Custom Jinja2 template for post generation
        """
        self.output_dir = Path(output_dir).resolve()  # Cross-platform path handling
        self.timezone = timezone
        self.template_engine = JekyllTemplateEngine(custom_template)
        self._setup_logging()
        self._validate_timezone()
        self._validate_output_directory()
    
    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger(__name__)
    
    def _validate_timezone(self) -> None:
        """Validate that the specified timezone exists."""
        try:
            ZoneInfo(self.timezone)
        except ZoneInfoNotFoundError:
            raise PostGeneratorError(
                f"Timezone '{self.timezone}' not found. "
                "Try installing the 'tzdata' package with: pip install tzdata"
            )
    
    def _validate_output_directory(self) -> None:
        """Validate output directory is writable."""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            # Test write permissions
            test_file = self.output_dir / '.test_write_permission'
            test_file.touch()
            test_file.unlink()
        except (OSError, PermissionError) as e:
            raise PostGeneratorError(f"Cannot write to output directory '{self.output_dir}': {e}")
    
    def _generate_filename(self, title: str, post_date: datetime) -> str:
        """Generate a Jekyll-compatible filename."""
        date_part = post_date.strftime("%Y-%m-%d")
        slug = slugify(title, max_length=50)
        
        if not slug:
            raise PostGeneratorError("Title produces empty slug - please use a different title")
        
        return f"{date_part}-{slug}.md"
    
    def _check_post_exists(self, filepath: Path, force: bool = False) -> bool:
        """
        Check if post already exists and handle accordingly.
        
        Args:
            filepath: Path to the post file
            force: If True, overwrite without asking
            
        Returns:
            True if should proceed, False otherwise
        """
        if not filepath.exists():
            return True
        
        if force:
            self.logger.info(f"🔄 Overwriting existing post: {filepath.name}")
            return True
        
        # Interactive confirmation
        try:
            response = input(f"⚠️  Post '{filepath.name}' already exists. Overwrite? (y/N): ")
            return response.lower().startswith('y')
        except (EOFError, KeyboardInterrupt):
            return False
    
    def _prepare_template_data(self, title: str, top_category: str, sub_category: str,
                              tags: List[str], post_date: datetime,
                              author: Optional[str] = None,
                              description: Optional[str] = None,
                              custom_fields: Optional[Dict[str, str]] = None) -> Dict:
        """Prepare data for template rendering."""
        # Format date for Jekyll
        formatted_date = post_date.strftime("%Y-%m-%d %H:%M:%S %z")
        
        # Prepare template data
        template_data = {
            'title': title,
            'date': formatted_date,
            'categories': [top_category, sub_category],
            'tags': tags,
        }
        
        # Add optional fields
        if author:
            template_data['author'] = author
        
        if description:
            template_data['description'] = description
        
        if custom_fields:
            template_data['custom_fields'] = custom_fields
        
        return template_data
    
    def generate(self, title: str, top_category: str, sub_category: str,
                 tags_input: str, author: Optional[str] = None,
                 description: Optional[str] = None,
                 custom_date: Optional[str] = None,
                 custom_fields: Optional[Dict[str, str]] = None,
                 force: bool = False) -> str:
        """
        Generate a Jekyll post with comprehensive validation.
        
        Args:
            title: Post title
            top_category: Primary category
            sub_category: Secondary category
            tags_input: Comma-separated tags
            author: Post author (optional)
            description: Post description (optional)
            custom_date: Custom date in YYYY-MM-DD format (optional)
            custom_fields: Additional custom fields for front matter
            force: Force overwrite existing files
            
        Returns:
            Path to the generated file
            
        Raises:
            PostGeneratorError: If generation fails
        """
        try:
            # Input validation
            validated_title = InputValidator.validate_title(title)
            validated_top_category = InputValidator.validate_category(top_category, "top category")
            validated_sub_category = InputValidator.validate_category(sub_category, "sub category")
            validated_tags = InputValidator.validate_tags(tags_input)
            validated_author = InputValidator.validate_author(author or "")
            validated_description = InputValidator.validate_description(description or "")
            
            # Handle date
            if custom_date:
                post_date = InputValidator.validate_date(custom_date)
                post_date = post_date.replace(tzinfo=ZoneInfo(self.timezone))
            else:
                post_date = datetime.now(ZoneInfo(self.timezone))
            
            # Generate filename and full path
            filename = self._generate_filename(validated_title, post_date)
            filepath = self.output_dir / filename
            
            # Check if post exists
            if not self._check_post_exists(filepath, force):
                self.logger.info("❌ Operation cancelled")
                return str(filepath)
            
            # Prepare template data
            template_data = self._prepare_template_data(
                validated_title, validated_top_category, validated_sub_category,
                validated_tags, post_date, validated_author or None,
                validated_description or None, custom_fields
            )
            
            # Render template
            content = self.template_engine.render_post(**template_data)
            
            # Write file with cross-platform path handling
            with open(filepath, "w", encoding="utf-8", newline='\n') as file:
                file.write(content)
            
            self.logger.info(f"✅ Jekyll post generated successfully: {filepath}")
            return str(filepath)
            
        except Exception as e:
            if isinstance(e, PostGeneratorError):
                raise
            raise PostGeneratorError(f"Failed to generate post: {str(e)}")


def load_custom_template(template_path: str) -> str:
    """Load custom template from file."""
    try:
        template_file = Path(template_path)
        if not template_file.exists():
            raise PostGeneratorError(f"Template file not found: {template_path}")
        
        return template_file.read_text(encoding='utf-8')
    except Exception as e:
        raise PostGeneratorError(f"Failed to load template: {e}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate Jekyll posts with Jinja2 templates and comprehensive validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "My New Post" "Tech" "Python" "python,tutorial"
  %(prog)s "Travel Blog" "Lifestyle" "Travel" "vacation,photography" --author "John Doe"
  %(prog)s "Old Post" "Tech" "AI" "machine-learning" --date "2023-01-15" --force
  %(prog)s "Custom Post" "Tech" "Web" "html,css" --template "custom_template.j2"
        """
    )
    
    # Required arguments
    parser.add_argument("title", help="Title of the post")
    parser.add_argument("top_category", help="Primary category of the post")
    parser.add_argument("sub_category", help="Secondary category of the post")
    parser.add_argument("tag", help="Comma-separated tags for the post")
    
    # Optional arguments
    parser.add_argument(
        "--output-dir", "-o",
        default=PostGenerator.DEFAULT_OUTPUT_DIR,
        help=f"Directory where the post will be saved (default: {PostGenerator.DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--timezone", "-tz",
        default=PostGenerator.DEFAULT_TIMEZONE,
        help=f"Timezone for timestamps (default: {PostGenerator.DEFAULT_TIMEZONE})"
    )
    parser.add_argument(
        "--author", "-a",
        help="Author of the post"
    )
    parser.add_argument(
        "--description", "-d",
        help="Description of the post (max 500 characters)"
    )
    parser.add_argument(
        "--date",
        help="Custom date for the post (YYYY-MM-DD format)"
    )
    parser.add_argument(
        "--template", "-t",
        help="Path to custom Jinja2 template file"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force overwrite existing posts without confirmation"
    )
    parser.add_argument(
        "--custom-field",
        action="append",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Add custom field to front matter (can be used multiple times)"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="Jekyll Post Generator 3.0 (Enhanced with Jinja2 & Validation)"
    )
    
    args = parser.parse_args()
    
    try:
        # Load custom template if provided
        custom_template = None
        if args.template:
            custom_template = load_custom_template(args.template)
        
        # Prepare custom fields
        custom_fields = {}
        if args.custom_field:
            for key, value in args.custom_field:
                custom_fields[key] = value
        
        # Initialize generator
        generator = PostGenerator(
            output_dir=args.output_dir,
            timezone=args.timezone,
            custom_template=custom_template
        )
        
        # Generate post
        filepath = generator.generate(
            title=args.title,
            top_category=args.top_category,
            sub_category=args.sub_category,
            tags_input=args.tag,
            author=args.author,
            description=args.description,
            custom_date=args.date,
            custom_fields=custom_fields if custom_fields else None,
            force=args.force
        )
        
        print(f"\n🎉 Post created: {filepath}")
        
    except PostGeneratorError as e:
        logging.error(f"❌ {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()