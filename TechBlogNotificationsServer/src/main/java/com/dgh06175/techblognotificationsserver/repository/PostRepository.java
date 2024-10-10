package com.dgh06175.techblognotificationsserver.repository;

import com.dgh06175.techblognotificationsserver.domain.Post;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PostRepository extends JpaRepository<Post, Long> {
    List<Post> findAllByLinkIn(List<String> links);
}
