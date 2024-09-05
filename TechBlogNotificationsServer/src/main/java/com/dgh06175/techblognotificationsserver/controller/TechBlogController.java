package com.dgh06175.techblognotificationsserver.controller;

import com.dgh06175.techblognotificationsserver.domain.Post;
import com.dgh06175.techblognotificationsserver.repository.PostRepository;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class TechBlogController {

    private final PostRepository postRepository;

    @GetMapping("posts")
    @ResponseBody
    public List<Post> findAll() {
        return postRepository.findAll();
    }
}
