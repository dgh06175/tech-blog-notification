package com.dgh06175.techblognotificationsserver.config.html;


import com.dgh06175.techblognotificationsserver.config.BlogConfig;
import com.dgh06175.techblognotificationsserver.domain.Post;
import org.jsoup.nodes.Element;

public class Inflab implements BlogConfig {
    @Override
    public String getBlogName() {
        return "Inflab";
    }

    @Override
    public String getBlogUrl() {
        return "https://tech.inflab.com";
    }

    @Override
    public String getListTagName() {
        return "div.post-card-wrapper";
    }

    @Override
    public Post parseElement(Element element) {
        String link = this.getBlogUrl() + element.select("a").attr("href");

        String title = element.select("div.title").text();

        String date = element.select("div.date").text().replaceAll("\\.", "-");
        return new Post(this.getBlogName(), link, title, date);
    }
}