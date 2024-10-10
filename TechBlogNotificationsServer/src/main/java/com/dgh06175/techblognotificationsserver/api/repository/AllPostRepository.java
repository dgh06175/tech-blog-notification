package com.dgh06175.techblognotificationsserver.api.repository;

import com.dgh06175.techblognotificationsserver.api.domain.Post;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AllPostRepository extends JpaRepository<Post, Long> {
}
