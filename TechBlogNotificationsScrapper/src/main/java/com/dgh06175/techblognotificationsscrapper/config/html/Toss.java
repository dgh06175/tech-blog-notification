package com.dgh06175.techblognotificationsscrapper.config.html;

import com.dgh06175.techblognotificationsscrapper.config.BlogConfig;
import com.dgh06175.techblognotificationsscrapper.domain.Post;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Toss implements BlogConfig {
    @Override
    public String getBlogName() {
        return "Toss";
    }

    @Override
    public String getBlogUrl() {
        return "https://toss.tech";
    }

    @Override
    public String getListTagName() {
        return "a.css-1qr3mg1.e1sck7qg4";
    }

    @Override
    public Post parseElement(Element element) {
        String link = this.getBlogUrl() + element.select("a").attr("href");

        Element titleSpan = element.select("a").select("div > span").first();
        String title = titleSpan != null ? titleSpan.text() : "";

        Element dateSpan = element.select("a").first();
        String date = extractDate(dateSpan);

        return new Post(this.getBlogName(), link, title, date);
    }

    // MARK: 주어진 element에서 여러개의 span 태그 중에 정규표현식으로 날짜 형식에 알맞은 텍스트 반환
    private String extractDate(Element element) {
        if (element == null) {
            return "";
        }

        Elements spans = element.select("span");
        Pattern pattern = Pattern.compile("\\d{4}\\D+\\d{1,2}\\D+\\d{1,2}");

        return spans.stream()
                .map(span -> pattern.matcher(span.text()))
                .filter(Matcher::find)
                .map(Matcher::group)
                .findFirst()
                .orElse("");
    }
}