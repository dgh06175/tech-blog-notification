package com.dgh06175.techblognotificationsserver.controller;

import com.dgh06175.techblognotificationsserver.config.*;
import com.dgh06175.techblognotificationsserver.config.html.Toss;
import com.dgh06175.techblognotificationsserver.config.rss.Kakao;
import com.dgh06175.techblognotificationsserver.config.rss.Woowahan;
import com.dgh06175.techblognotificationsserver.domain.Post;
import com.dgh06175.techblognotificationsserver.repository.PostRepository;
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
        List<Post> posts = parse(blogConfigs);
//        posts.sort(Post::getPubDate);
        for (Post post : posts) {
            post.printPost();
            System.out.println();
        }

        // 2. DB에 중복 데이터 제외하고 추가하기
        savePosts(posts);
    }

    public List<Post> parse(List<BlogConfig> blogConfigs) {
        List<Post> posts = new ArrayList<>();
        for (BlogConfig blogConfig : blogConfigs) {
            try {
                Document document = Jsoup.connect(blogConfig.getBlogUrl()).get();
                Elements items = document.select(blogConfig.getListTagName());
                for (Element item : items) {
                    posts.add(blogConfig.parseElement(item));
                }
            } catch (Exception e) {
                logger.warn(String.format("%s %s", "ScrapController ERROR", e.getMessage()));
            }
        }

        return posts;
    }

    private void savePosts(List<Post> posts) {
        for (Post post : posts) {
            if (postRepository.findByLink(post.getLink()) == null) {
                postRepository.save(post);
            }
        }
    }
}
