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
import java.io.IOException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;

@Controller
public class ScrapController {
    private static final Logger logger = LoggerFactory.getLogger(ScrapController.class.getName());

    @Autowired
    private PostRepository postRepository;

    public void run() {
        // 1. 블로그에서 포스트 불러오기
        List<BlogConfig> blogConfigs = new ArrayList<>();
        blogConfigs.add(new Toss());
        blogConfigs.add(new Woowahan());
        blogConfigs.add(new Kakao());
        try {
            List<Post> posts = parse(blogConfigs);
            // 2. DB에 중복 데이터 제외하고 추가하기
            savePosts(posts);
        } catch (ScrapException e) {
            logger.warn(e.getMessage());
        }
    }

    public List<Post> parse(List<BlogConfig> blogConfigs) throws ScrapException {
        List<Post> posts = new ArrayList<>();
        for (BlogConfig blogConfig : blogConfigs) {
            try {
                Document document = Jsoup.connect(blogConfig.getBlogUrl()).get();
                Elements items = document.select(blogConfig.getListTagName());
                if (items.isEmpty()) {
                    throw new ScrapParsingException(blogConfig.getBlogUrl());
                } else {
                    for (Element item : items) {
                        Post post = blogConfig.parseElement(item);
                        if (post.getTitle().isEmpty() || post.getLink().equals(blogConfig.getBlogUrl())) {
                            post.printPost();
                            throw new ScrapParsingException(blogConfig.getBlogUrl());
                        }
                        posts.add(post);
                    }
                }
            } catch (UnknownHostException e2) {
                throw new ScrapHttpException(blogConfig.getBlogUrl());
            } catch (IOException e) {
                throw new ScrapException(e.getLocalizedMessage());
            }
        }

        return posts;
    }

    private void savePosts(List<Post> posts) {
        int count = 0;
        for (Post post : posts) {
            if (postRepository.findByLink(post.getLink()) == null) {
                count += 1;
                System.out.println("포스트 저장됨: " + post.getLink());
                post.printPost();
                System.out.println();
                postRepository.save(post);
            }
        }
        System.out.printf("%d 개의 포스트 저장됨\n", count);
    }
}
