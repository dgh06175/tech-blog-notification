package org.example.parser;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;
import org.jsoup.nodes.Element;


public class XMLBlogParser extends AbstractJsoupBlogParser {
    @Override
    protected String getItemTagName() {
        return "item";
    }

    @Override
    protected Map<String, String> parseElement(Element element) {
        Map<String, String> article = new HashMap<>();

        article.put("link", element.select("link").text()); // 'link' 태그
        article.put("title", element.select("title").text()); // 'title' 태그
        article.put("author", element.select("dc\\:creator").text()); // 'dc:creator' 태그 처리
        String pubDate = element.select("pubDate").text();
        article.put("date", formattedDate(pubDate)); // 'pubDate' 태그

        return article;
    }

    /// MARK: 날짜 형식 바꿔주는 함수 ("Wed, 24 Apr 2024 06:00:53 +0000" -> "2024. 04. 24")
    private String formattedDate(String inputDate) {
        SimpleDateFormat inputFormat = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss Z", Locale.ENGLISH);
        SimpleDateFormat outputFormat = new SimpleDateFormat("yyyy. MM. dd");
        try {
            Date date = inputFormat.parse(inputDate);
            return outputFormat.format(date);
        } catch (ParseException e) {
            e.printStackTrace();
            return null;
        }
    }
}
