package org.example.service.parser;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class TossBlogParser extends AbstractJsoupBlogParser {

    @Override
    protected String getItemTagName() {
        return "ul.css-nsslhm.e16omkx80 li";
    }

    @Override
    protected Map<String, String> parseElement(Element element) {
        Map<String, String> article = new HashMap<>();
        String link = "https://toss.tech" + element.select("a").attr("href");
        Element titleSpan = element.select("a").select("div > span").first();
        String title = titleSpan != null ? titleSpan.text() : "";
        String author = ""; // 저자 정보가 없음
        Element dateSpan = element.select("a").first();
        String date = extractDate(dateSpan);

        article.put("link", link);
        article.put("title", title);
        article.put("author", author);
        article.put("date", date);
        return article;
    }

    /// MARK: 주어진 element에서 여러개의 span 태그 중에 정규표현식으로 날짜 형식에 알맞은 텍스트 반환
    private String extractDate(Element element) {
        if (element == null) {
            return "";
        }
        Elements spans = element.select("span");
        Pattern pattern = Pattern.compile("\\d{4}\\. \\d{1,2}\\. \\d{1,2}");
        for (Element span : spans) {
            Matcher matcher = pattern.matcher(span.text());
            if (matcher.find()) {
                return matcher.group();
            }
        }
        return "";
    }
}
