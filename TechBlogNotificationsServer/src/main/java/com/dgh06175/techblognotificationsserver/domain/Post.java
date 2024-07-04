package com.dgh06175.techblognotificationsserver.domain;

import com.dgh06175.techblognotificationsserver.utils.DateParser;
import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Objects;
import lombok.Data;

@Data
@Entity
public class Post {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String link;

    private String blogName;

    private String title;

    private LocalDate pubDate;

    private LocalDate scrapedDate;

    public Post(){}

    public Post(String blogName, String link, String title, String dateString) {
        this.blogName = blogName;
        this.link = link;
        this.title = title;
        this.pubDate = DateParser.parseDate(dateString);
        this.scrapedDate = LocalDate.now();
    }

    public void printPost() {
        System.out.printf("blogName: %s%n", blogName);
        System.out.printf("title: %s%n", title);
        System.out.printf("link: %s%n", link);
        System.out.printf("pubDate: %s%n", pubDate != null ? pubDate.toString() : "N/A");
        System.out.printf("scrapedDate: %s%n", scrapedDate);
    }

    // MARK: - 링크가 동일한 게시물을 같은 게시물로 취급함.
    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        Post post = (Post) o;
        return Objects.equals(link, post.link);
    }

    @Override
    public int hashCode() {
        return Objects.hash(link);
    }
}
