package org.example.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Locale;
import java.util.Objects;

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
//    private final LocalDate date;

    public Article(String link, String title, String author, String dateString) {
        this.link = link;
        this.title = title;
        this.author = author;
        this.localDate = parseDate(dateString);
        if (localDate != null) {
            this.date = localDate.format(DateTimeFormatter.ofPattern("yyyy. M. d", Locale.ENGLISH));
        } else {
            this.date = null;  // 또는 기본 날짜 지정
        }

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
                return null;
//                throw new IllegalArgumentException("날짜 형식이 올바르지 않습니다." + dateString);
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
        return Objects.equals(link, article.link) &&
                Objects.equals(title, article.title) &&
                Objects.equals(author, article.author) &&
                Objects.equals(date, article.date);
    }

    @Override
    public int hashCode() {
        return Objects.hash(link, title, author, date);
    }
}
