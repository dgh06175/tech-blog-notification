package com.dgh06175.techblognotificationsserver;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class TechBlogNotificationsServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(TechBlogNotificationsServerApplication.class, args);
    }
}
