package com.dgh06175.techblognotificationsserver.repository;

import com.dgh06175.techblognotificationsserver.domain.Post;
import java.util.List;

public interface PostRepository {
    Post save(Post post);
    List<Post> findAll();
}
