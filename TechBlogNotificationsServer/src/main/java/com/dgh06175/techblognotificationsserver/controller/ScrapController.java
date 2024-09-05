package com.dgh06175.techblognotificationsserver.controller;

import com.dgh06175.techblognotificationsserver.config.*;
import com.dgh06175.techblognotificationsserver.config.html.Toss;
import com.dgh06175.techblognotificationsserver.config.rss.Kakao;
import com.dgh06175.techblognotificationsserver.config.rss.Woowahan;
import com.dgh06175.techblognotificationsserver.domain.Post;
import com.dgh06175.techblognotificationsserver.exception.ScrapException;
import com.dgh06175.techblognotificationsserver.exception.ScrapHttpException;
import com.dgh06175.techblognotificationsserver.exception.ScrapParsingException;
import com.dgh06175.techblognotificationsserver.repository.PostRepository;
import com.dgh06175.techblognotificationsserver.service.PostService;
import java.io.IOException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
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
