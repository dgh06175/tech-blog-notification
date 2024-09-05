package com.dgh06175.techblognotificationsserver.repository;

import com.dgh06175.techblognotificationsserver.domain.Post;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface PostRepository extends PagingAndSortingRepository<Post, Long> {}
