package com.dgh06175.techblognotificationsscrapper.controller;

import com.dgh06175.techblognotificationsscrapper.config.BlogConfig;
import com.dgh06175.techblognotificationsscrapper.config.html.Toss;
import com.dgh06175.techblognotificationsscrapper.config.rss.Kakao;
import com.dgh06175.techblognotificationsscrapper.config.rss.Woowahan;
import com.dgh06175.techblognotificationsscrapper.service.PostService;
import java.util.ArrayList;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;

@Controller
@RequiredArgsConstructor
public class ScrapController {
    private final PostService postService;

    public void scrapPosts() {
        // 1. 블로그에서 포스트 불러오기
        List<BlogConfig> blogConfigs = new ArrayList<>();
        blogConfigs.add(new Toss());
        blogConfigs.add(new Woowahan());
        blogConfigs.add(new Kakao());

        // 2. 스크랩한 정보 DB에 저장하기
        postService.scrapPosts(blogConfigs);
    }
}
