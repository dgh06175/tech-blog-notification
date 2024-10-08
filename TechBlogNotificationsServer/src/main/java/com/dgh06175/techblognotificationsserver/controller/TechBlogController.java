package com.dgh06175.techblognotificationsserver.controller;

import com.dgh06175.techblognotificationsserver.domain.Post;
import com.dgh06175.techblognotificationsserver.repository.AllPostRepository;
import com.dgh06175.techblognotificationsserver.repository.PostRepository;
import java.util.ArrayList;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
public class TechBlogController {

    private final PostRepository postRepository;
    private final AllPostRepository allPostRepository;

    @GetMapping("all-post")
    public List<Post> getAllPosts() {
        return allPostRepository.findAll();
    }

    @GetMapping("posts")
    public List<Post> getPosts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        List<Sort.Order> orders = new ArrayList<>();
        orders.add(new Sort.Order(Sort.Direction.DESC, "pubDate"));

        Pageable pageable = PageRequest.of(page, size, Sort.by(orders));
        return postRepository.findAll(pageable).getContent();
    }
}
