package com.dgh06175.techblognotificationsserver.api.repository;

import com.dgh06175.techblognotificationsserver.api.domain.Post;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface PostRepository extends PagingAndSortingRepository<Post, Long> {}
