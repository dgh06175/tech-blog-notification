package com.dgh06175.techblognotificationsserver.service;

import static org.assertj.core.api.Assertions.assertThatCode;

import com.dgh06175.techblognotificationsserver.config.BlogConfig;
import com.dgh06175.techblognotificationsserver.config.html.Inflab;
import com.dgh06175.techblognotificationsserver.config.html.KakaoBank;
import com.dgh06175.techblognotificationsserver.config.html.Toss;
import com.dgh06175.techblognotificationsserver.config.rss.Kakao;
import com.dgh06175.techblognotificationsserver.config.rss.Woowahan;
import com.dgh06175.techblognotificationsserver.domain.Post;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@Transactional
class PostServiceTest {

    @Autowired
    private PostService postService;

    @Test
    void 카카오_게시글_스크랩_테스트() {
        BlogConfig blogConfig = new Kakao();
        assertThatCode(() -> {
            List<Post> posts = postService.scrapPosts(blogConfig);
            for (Post post : posts) {
                post.print();
            }
        }).doesNotThrowAnyException();
    }

    @Test
    void 토스_게시글_스크랩_테스트() {
        BlogConfig blogConfig = new Toss();
        assertThatCode(() -> {
            List<Post> posts = postService.scrapPosts(blogConfig);
            for (Post post : posts) {
                post.print();
            }
        }).doesNotThrowAnyException();
    }

    @Test
    void 우아한_게시글_스크랩_테스트() {
        BlogConfig blogConfig = new Woowahan();
        assertThatCode(() -> {
            List<Post> posts = postService.scrapPosts(blogConfig);
            for (Post post : posts) {
                post.print();
            }
        }).doesNotThrowAnyException();
    }

    @Test
    void 인프랩_게시글_스크랩_테스트() {
        BlogConfig blogConfig = new Inflab();
        assertThatCode(() -> {
            List<Post> posts = postService.scrapPosts(blogConfig);
            for (Post post : posts) {
                post.print();
            }
        }).doesNotThrowAnyException();
    }

    @Test
    void 카카오뱅크_게시글_스크랩_테스트() {
        BlogConfig blogConfig = new KakaoBank();
        assertThatCode(() -> {
            List<Post> posts = postService.scrapPosts(blogConfig);
            for (Post post : posts) {
                post.print();
            }
        }).doesNotThrowAnyException();
    }
}