package org.example.model;

import java.util.*;

public class Articles {
    public final String blogName;

    private final LinkedHashSet<Article> articles;

    public Articles(Set<Article> articles, String blogName) {
        this.articles = new LinkedHashSet<>(articles);
        this.blogName = blogName;
    }

    public Articles(List<Article> articles, String blogName) {
        this.articles = new LinkedHashSet<>(articles);
        this.blogName = blogName;
    }

    public void printArticles() {
        for (var article : articles) {
            article.printArticle();
        }
    }

    public Set<Article> getArticles() {
        return Collections.unmodifiableSet(articles);
    }

    // MARK: - 아티클 데이터에서 새로운 아티클 정보를 뺀 아티클들을 반환한다.
    public Articles filterNewArticles(Articles newArticles) {
        LinkedHashSet<Article> newArticlesSet = new LinkedHashSet<>(newArticles.articles);
        newArticlesSet.removeAll(this.articles);
        return new Articles(newArticlesSet, this.blogName);
    }

    public Articles sumArticles(Articles newArticles) {
        LinkedHashSet<Article> newArticlesSet = newArticles.articles;
        newArticlesSet.addAll(this.articles);
        return new Articles(newArticlesSet, this.blogName);
    }
}
