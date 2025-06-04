import argparse
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import os
import sys

class PostGenerator:
    def generate(self, title, top_category, sub_category, tag):
        try:
            # Try to use Asia/Kolkata timezone
            now = datetime.now(ZoneInfo("Asia/Kolkata"))
        except ZoneInfoNotFoundError:
            print("❌ Error: Timezone 'Asia/Kolkata' not found.")
            print("🔧 Try installing the 'tzdata' package with:")
            print("   pip install tzdata")
            sys.exit(1)

        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S %z")
        date_part = now.strftime("%Y-%m-%d")
        filename = f"_posts/{date_part}-{title.lower().replace(' ', '-')}.md"

        content = f"""---
title: {title}
date: {formatted_date}
categories: [{top_category}, {sub_category}]
tags: [{tag.lower()}]
---
"""

        os.makedirs("_posts", exist_ok=True)
        with open(filename, "w") as file:
            file.write(content)

        print("✅ Jekyll post generated successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Jekyll post")
    parser.add_argument("title", help="Title of the post")
    parser.add_argument("top_category", help="Top category of the post")
    parser.add_argument("sub_category", help="Sub-category of the post")
    parser.add_argument("tag", help="Tag for the post")

    args = parser.parse_args()

    generator = PostGenerator()
    generator.generate(args.title, args.top_category, args.sub_category, args.tag)
