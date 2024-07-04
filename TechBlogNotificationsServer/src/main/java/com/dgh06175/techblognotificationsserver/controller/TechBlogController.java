package com.dgh06175.techblognotificationsserver.controller;

import com.dgh06175.techblognotificationsserver.domain.Post;
import com.dgh06175.techblognotificationsserver.repository.PostRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class TechBlogController {

    @Autowired
    private PostRepository postRepository;

    @GetMapping("find-all")
    @ResponseBody
    public List<Post> findAll() {
        List<Post> posts = postRepository.findAll();
        return posts;
    }
}
