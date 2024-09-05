package com.dgh06175.techblognotificationsserver.service;

import com.dgh06175.techblognotificationsserver.config.BlogConfig;
import com.dgh06175.techblognotificationsserver.controller.ScrapController;
import com.dgh06175.techblognotificationsserver.domain.Post;
import com.dgh06175.techblognotificationsserver.exception.ScrapException;
import com.dgh06175.techblognotificationsserver.exception.ScrapHttpException;
import com.dgh06175.techblognotificationsserver.exception.ScrapParsingException;
import com.dgh06175.techblognotificationsserver.repository.PostRepository;
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
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class PostService {
    private static final Logger logger = LoggerFactory.getLogger(PostService.class.getName());

    private final PostRepository postRepository;

    public void scrapPosts(List<BlogConfig> blogConfigs) throws ScrapException {
        try {
            List<Post> posts = parse(blogConfigs);
            savePosts(posts);
        } catch (ScrapException e) {
            logger.warn(e.getMessage());
        }
    }

    private List<Post> parse(List<BlogConfig> blogConfigs) throws ScrapException {
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
