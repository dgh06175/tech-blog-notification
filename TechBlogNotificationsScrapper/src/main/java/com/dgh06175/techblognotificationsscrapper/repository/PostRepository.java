package com.dgh06175.techblognotificationsscrapper.repository;

import com.dgh06175.techblognotificationsscrapper.domain.Post;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PostRepository extends JpaRepository<Post, Long> {
    List<Post> findAllByLinkIn(List<String> links);
    Post findByLink(String link);
}
