package org.example.model;

import java.util.Collections;
import java.util.List;
import java.util.Map;

public class Articles {
    public final String blogName;

    private final List<Map<String, String>> articles;

    public Articles(List<Map<String, String>> articles, String blogName) {
        this.articles = articles;
        this.blogName = blogName;
    }

    public void printArticles() {
        for (var article : articles) {
            System.out.println(article);
        }
    }

    public List<Map<String, String>> getArticles() {
        return Collections.unmodifiableList(articles);
    }
}
