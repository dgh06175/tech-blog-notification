package org.example;

import java.util.List;
import java.util.Map;
import org.example.service.parser.TossHTMLBlogParser;
import org.example.service.parser.XMLBlogParser;

public class Main {
    public static void main(String[] args) {
        XMLBlogParser XMLBlogParser = new XMLBlogParser();
        List<Map<String, String>> woowahanArticles = XMLBlogParser.parse("https://techblog.woowahan.com/rss/");
        System.out.println("우아한 형제들 블로그");
        for (var article : woowahanArticles) {
            System.out.println(article);
        }

        TossHTMLBlogParser tossHTMLBlogParser = new TossHTMLBlogParser();
        List<Map<String, String>> tossArticles = tossHTMLBlogParser.parse("https://toss.tech/");
        System.out.println("토스 블로그");
        for (var article : tossArticles) {
            System.out.println(article);
        }

        List<Map<String, String>> kakaoArticles = XMLBlogParser.parse("https://tech.kakao.com/feed");
        System.out.println("카카오 블로그");
        for (var article : kakaoArticles) {
            System.out.println(article);
        }
    }
}