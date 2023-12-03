class PostGenerator < Thor
  desc "generate TITLE TOP_CATEGORY SUB_CATEGORY TAG", "Generate a Jekyll post"
  def generate(title, top_category, sub_category, tag)
    formatted_date = Time.now.strftime("%Y-%m-%d %H:%M:%S %z")

    content = <<-POST
---
title: #{title}
date: #{formatted_date}
categories: [#{top_category}, #{sub_category}]
tags: [#{tag.downcase}]
---
    POST

    File.write("_posts/#{formatted_date.split(' ')[0]}-#{title.downcase.gsub(' ', '-')}.md", content)

    puts "Jekyll post generated successfully!"
  end
end
