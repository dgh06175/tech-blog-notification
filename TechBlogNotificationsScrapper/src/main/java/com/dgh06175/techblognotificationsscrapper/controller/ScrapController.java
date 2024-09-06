package com.dgh06175.techblognotificationsscrapper.controller;

import com.dgh06175.techblognotificationsscrapper.config.BlogConfig;
import com.dgh06175.techblognotificationsscrapper.domain.Post;
import com.dgh06175.techblognotificationsscrapper.service.PostService;
import java.io.IOException;
import java.util.List;
import java.util.Scanner;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;

@Controller
@RequiredArgsConstructor
public class ScrapController {
    private final PostService postService;

    public void run() {
        List<BlogConfig> blogConfigs = postService.getBlogConfigs();

        List<Post> scrapedPosts = postService.scrapPosts(blogConfigs);

        postService.savePosts(scrapedPosts);
    }
}
