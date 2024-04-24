package org.example.parser;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class TossHTMLBlogParser extends AbstractJsoupBlogParser {

    @Override
    protected String getItemTagName() {
        return "ul.css-nsslhm.e16omkx80 li";
    }

    @Override
    protected Map<String, String> parseElement(Element element) {
        Map<String, String> article = new HashMap<>();
        Element titleSpan = element.select("a").select("div > span").first();
        String title = titleSpan != null ? titleSpan.text() : "";
        Element dateSpan = element.select("a").first();
        String date = extractDate(dateSpan);

        article.put("link", "https://toss.tech" + element.select("a").attr("href"));
        article.put("title", title);
        article.put("author", ""); // 작성자 정보 없음
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
