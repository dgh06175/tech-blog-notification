package com.dgh06175.techblognotificationsserver.repository;

import com.dgh06175.techblognotificationsserver.domain.Post;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AllPostRepository extends JpaRepository<Post, Long> {
}
