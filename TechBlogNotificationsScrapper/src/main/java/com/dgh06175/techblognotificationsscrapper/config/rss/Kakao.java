package com.dgh06175.techblognotificationsscrapper.config.rss;

import com.dgh06175.techblognotificationsscrapper.config.BlogConfig;
import com.dgh06175.techblognotificationsscrapper.domain.Post;
import org.jsoup.nodes.Element;

public class Kakao implements BlogConfig {
    @Override
    public String getBlogName() {
        return "Kakao";
    }

    @Override
    public String getBlogUrl() {
        return "https://tech.kakao.com/blog/feed";
    }

    @Override
    public String getListTagName() {
        return "item";
    }

    @Override
    public Post parseElement(Element element) {
        String link = element.select("link").text();
        String title = element.select("title").text();
        String date = element.select("pubDate").text();
        return new Post(getBlogName(), link, title, date);
    }
}
