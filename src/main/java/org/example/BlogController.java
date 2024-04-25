package org.example;

import java.util.ArrayList;
import java.util.List;
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
    private static final String KAKAO_NAME = "KaKao";

    DataManager dataManager;

    public BlogController() {
        this.dataManager = new DataManager();
    }

    public void run() {
//        List<Articles> blogArticles = loadArticlesFromWeb();
//        blogArticles.forEach(this::saveArticlesToDB);
        readArticlesFromDB().forEach(Articles::printArticles);
    }

    private List<Articles> readArticlesFromDB() {
        return List.of(dataManager.readArticlesFromJsonFile(WOOWAHAN_NAME),
                dataManager.readArticlesFromJsonFile(TOSS_NAME),
                dataManager.readArticlesFromJsonFile(KAKAO_NAME));
    }

    private List<Articles> loadArticlesFromWeb() {
        XMLBlogParser XMLBlogParser = new XMLBlogParser();
        TossHTMLBlogParser tossHTMLBlogParser = new TossHTMLBlogParser();
        List<Articles> blogArticles = new ArrayList<>();

        blogArticles.add(XMLBlogParser.parse(WOOWAHAN_LINK, WOOWAHAN_NAME));
        blogArticles.add(tossHTMLBlogParser.parse(TOSS_LINK, TOSS_NAME));
        blogArticles.add(XMLBlogParser.parse(KAKAO_LINK, KAKAO_NAME));

        return blogArticles;
    }

    private void saveArticlesToDB(Articles articles) {
        dataManager.saveArticlesToJsonFile(articles);
    }
}
