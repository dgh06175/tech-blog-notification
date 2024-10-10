package com.dgh06175.techblognotificationsserver.controller;

import com.dgh06175.techblognotificationsserver.config.BlogConfig;
import com.dgh06175.techblognotificationsserver.domain.Post;
import com.dgh06175.techblognotificationsserver.service.PostService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
public class TechBlogController {

    private final PostService postService;

    @GetMapping("posts")
    public List<Post> getPosts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {

        return postService.findAll(page, size);
    }

    @Scheduled(cron = "0 0 5 * * *", zone = "Asia/Seoul")
    public void scrapPosts() {
        List<BlogConfig> blogConfigs = postService.getBlogConfigs();

        List<Post> scrapedPosts = postService.scrapPosts(blogConfigs);

        postService.savePosts(scrapedPosts);
    }
}
