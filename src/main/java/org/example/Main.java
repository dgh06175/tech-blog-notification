package org.example;

import java.util.List;
import java.util.Map;
import org.example.service.parser.TossBlogParser;
import org.example.service.parser.WoowahanBlogParser;

public class Main {
    public static void main(String[] args) {
        WoowahanBlogParser woowahanBlogParser = new WoowahanBlogParser();
        List<Map<String, String>> woowahanArticles = woowahanBlogParser.parse("https://techblog.woowahan.com/rss/");
        System.out.println("우아한 형제들 블로그");
        for (var article : woowahanArticles) {
            System.out.println(article);
        }

        TossBlogParser tossBlogParser = new TossBlogParser();
        List<Map<String, String>> articles = tossBlogParser.parse("https://toss.tech/");
        System.out.println("토스 블로그");
        for (var article : articles) {
            System.out.println(article);
        }
    }
}