package com.dgh06175.techblognotificationsserver.config.rss;

import com.dgh06175.techblognotificationsserver.config.BlogConfig;
import com.dgh06175.techblognotificationsserver.domain.Post;
import org.jsoup.nodes.Element;

final public class Woowahan implements BlogConfig {
    @Override
    public String getBlogName() {
        return "Woowahan";
    }

    @Override
    public String getBlogUrl() {
        return "https://techblog.woowahan.com/rss/";
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
