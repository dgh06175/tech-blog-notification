package com.dgh06175.techblognotificationsscrapper.repository;

import com.dgh06175.techblognotificationsscrapper.domain.Post;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PostRepository extends JpaRepository<Post, Long> {
    Post findByLink(String link);
}
