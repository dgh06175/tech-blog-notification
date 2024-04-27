package org.example;

import java.util.*;
import org.example.model.Articles;
import org.example.model.DataManager;
import org.example.parser.TossHTMLBlogParser;
import org.example.parser.XMLBlogParser;

public class BlogController {
    private static final String WOOWAHAN_LINK = "https://techblog.woowahan.com/rss/";
    private static final String WOOWAHAN_NAME = "Woowahan";
    private static final String TOSS_LINK = "https://toss.tech/";
    private static final String TOSS_NAME = "Toss";
    private static final String KAKAO_LINK = "https://tech.kakao.com/feed";
    private static final String KAKAO_NAME = "Kakao";

    private final DataManager dataManager;

    public BlogController() {
        this.dataManager = new DataManager();
    }

    public void run() {
        Map<String, Articles> loadedBlogsArticles = loadArticlesFromWeb();
        Map<String, Articles> readBlogsArticles = readArticlesFromDB();
        List<Articles> newBlogsArticles = new ArrayList<>();
        List<Articles> oldBlogsArticles = new ArrayList<>();
        // loadedBlogsArticles 의 데이터들 중에 같은 블로그일 경우 filterNewArticles 를 사용해서 새로 나온 아티클들만 들어있는 Articles 를 만든다.
        for (var entry : loadedBlogsArticles.entrySet()) {
            String blogName = entry.getKey();
            Articles loadedArticles = entry.getValue();

            if (readBlogsArticles.containsKey(blogName)) {
                Articles readArticle = readBlogsArticles.get(blogName);
                newBlogsArticles.add(readArticle.filterNewArticles(loadedArticles));
                oldBlogsArticles.add(readArticle.sumArticles(loadedArticles));
            }
        }
        newBlogsArticles.forEach(this::saveNewArticlesToDatabase);
        oldBlogsArticles.forEach(this::saveOldArticlesToDatabase);
    }

    private Map<String, Articles> readArticlesFromDB() {
        Map<String, Articles> blogArticles = new HashMap<>();
        blogArticles.put(WOOWAHAN_NAME, dataManager.readArticlesFromJsonFile(WOOWAHAN_NAME));
        blogArticles.put(TOSS_NAME, dataManager.readArticlesFromJsonFile(TOSS_NAME));
        blogArticles.put(KAKAO_NAME, dataManager.readArticlesFromJsonFile(KAKAO_NAME));
        return blogArticles;
    }

    private Map<String, Articles> loadArticlesFromWeb() {
        XMLBlogParser XMLBlogParser = new XMLBlogParser();
        TossHTMLBlogParser tossHTMLBlogParser = new TossHTMLBlogParser();
        Map<String, Articles> blogArticles = new HashMap<>();
        Articles woowahanArticles = XMLBlogParser.parse(WOOWAHAN_LINK, WOOWAHAN_NAME);
        blogArticles.put(woowahanArticles.blogName, woowahanArticles);
        Articles tossArticles = tossHTMLBlogParser.parse(TOSS_LINK, TOSS_NAME);
        blogArticles.put(tossArticles.blogName, tossArticles);
        Articles kakaoArticles = XMLBlogParser.parse(KAKAO_LINK, KAKAO_NAME);
        blogArticles.put(kakaoArticles.blogName, kakaoArticles);

        return blogArticles;
    }

    private void saveOldArticlesToDatabase(Articles articles) {
        dataManager.saveOldArticlesToJsonFile(articles);
    }

    private void saveNewArticlesToDatabase(Articles articles) {
        dataManager.saveNewArticlesToJsonFile(articles);
    }
}
