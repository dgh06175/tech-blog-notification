package org.example.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Locale;
import java.util.Objects;

/**
 * 블로그의 게시글 하나의 정보
 */
public class Article {
    @JsonProperty("link")
    private final String link;
    @JsonProperty("title")
    private final String title;
    @JsonProperty("author")
    private final String author;
    @JsonProperty("date")
    private final String date;
    private final LocalDate localDate;

    public Article(String link, String title, String author, String dateString) {
        this.link = link;
        this.title = title;
        this.author = author;
        this.localDate = parseDate(dateString);
        this.date = localDate.format(DateTimeFormatter.ofPattern("yyyy. M. d", Locale.ENGLISH));

    }

    public void printArticle() {
        System.out.printf("link: %s%n", link);
        System.out.printf("title: %s%n", title);
        System.out.printf("author: %s%n", author);
        System.out.printf("date: %s%n", date);
    }

    private LocalDate parseDate(String dateString) {
        DateTimeFormatter formatterRFC1123 = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss Z", Locale.ENGLISH);
        DateTimeFormatter formatterCustom = DateTimeFormatter.ofPattern("yyyy. M. d", Locale.ENGLISH);

        try {
            return LocalDate.parse(dateString, formatterRFC1123);
        } catch (DateTimeParseException e) {
            try {
                return LocalDate.parse(dateString, formatterCustom);
            } catch (DateTimeParseException ex) {
                throw new IllegalArgumentException("날짜 형식이 올바르지 않습니다." + dateString);
            }
        }
    }


    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        Article article = (Article) o;
        return Objects.equals(link, article.link);
    }

    @Override
    public int hashCode() {
        return Objects.hash(link);
    }
}
