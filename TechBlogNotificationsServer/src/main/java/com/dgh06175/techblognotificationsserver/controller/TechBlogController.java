package com.dgh06175.techblognotificationsserver.controller;

import com.dgh06175.techblognotificationsserver.config.BlogConfig;
import com.dgh06175.techblognotificationsserver.domain.Post;
import com.dgh06175.techblognotificationsserver.service.PostService;
import java.util.ArrayList;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequiredArgsConstructor
public class TechBlogController {

    private final PostService postService;

    @GetMapping("posts")
    public List<Post> getPosts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        log.info("포스트 호출 발생 page: {}, size: {}", page, size);
        return postService.findAll(page, size);
    }

    @Scheduled(cron = "0 0 5 * * *", zone = "Asia/Seoul")
    public void scrapPosts() {
        log.info("게시글 스크랩 실행");
        List<BlogConfig> blogConfigs = postService.getBlogConfigs();

        List<Post> scrapedPosts = new ArrayList<>();
        for (BlogConfig blogConfig : blogConfigs) {
            scrapedPosts.addAll(postService.scrapPosts(blogConfig));
        }
        postService.savePosts(scrapedPosts);
    }
}
