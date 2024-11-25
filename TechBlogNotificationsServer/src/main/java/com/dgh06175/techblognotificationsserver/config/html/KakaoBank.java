package com.dgh06175.techblognotificationsserver.config.html;

import com.dgh06175.techblognotificationsserver.config.BlogConfig;
import com.dgh06175.techblognotificationsserver.domain.Post;
import org.jsoup.nodes.Element;

public class KakaoBank implements BlogConfig {
    @Override
    public String getBlogName() {
        return "KakaoBank";
    }

    @Override
    public String getBlogUrl() {
        return "https://tech.kakaobank.com";
    }

    @Override
    public String getListTagName() {
        return "div.post";
    }

    @Override
    public Post parseElement(Element element) {
        String link = this.getBlogUrl() + element.select("h2.post-item").select("a").attr("href")
                .substring(1);

        String title = element.select("h2.post-title").select("a").text();

        String date = element.select("div.post-info").select("div.date").text();
        return new Post(this.getBlogName(), link, title, date);
    }
}