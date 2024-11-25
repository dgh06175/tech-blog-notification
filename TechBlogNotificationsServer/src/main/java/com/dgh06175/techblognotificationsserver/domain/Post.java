package com.dgh06175.techblognotificationsserver.domain;

import com.dgh06175.techblognotificationsserver.utils.DateParser;
import jakarta.persistence.Entity;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import java.time.LocalDate;
import java.util.Objects;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

@Getter
@Setter
@NoArgsConstructor
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Post {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String link;

    private String blogName;

    private String title;

    private LocalDate pubDate;

    @CreatedDate
    private LocalDate scrapedDate;

    public Post(String blogName, String link, String title, String dateString) {
        this.blogName = blogName;
        this.link = link;
        this.title = title;
        this.pubDate = DateParser.parseDate(dateString);
    }

    public void print() {
        System.out.printf("blogName: %s%n", blogName);
        System.out.printf("title: %s%n", title);
        System.out.printf("link: %s%n", link);
        System.out.printf("pubDate: %s%n", pubDate != null ? pubDate.toString() : "N/A");
        System.out.println();
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
