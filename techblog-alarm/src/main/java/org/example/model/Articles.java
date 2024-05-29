package org.example.model;

import java.util.*;

/**
 * 특정 블로그 (blogName) 의 게시글(articles) 정보 모음
 */
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

    // MARK: - 새로운 아티클 정보에서 과거 아티클 데이터를 뺀 것들을 반환한다.
    public Articles filterNewArticles(Articles newArticles) {
        LinkedHashSet<Article> newArticlesSet = new LinkedHashSet<>(newArticles.articles);
        newArticlesSet.removeAll(this.articles);
        return new Articles(newArticlesSet, this.blogName);
    }

    // MARK: - 과거 아티클 데이터와 새로운 아티클 데이터를 합친다.
    public Articles sumArticles(Articles newArticles) {
        LinkedHashSet<Article> newArticlesSet = newArticles.articles;
        newArticlesSet.addAll(this.articles);
        return new Articles(newArticlesSet, this.blogName);
    }
}
