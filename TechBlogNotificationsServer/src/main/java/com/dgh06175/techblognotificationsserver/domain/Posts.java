//package com.dgh06175.techblognotificationsserver.domain;
//
//import java.util.*;
//
//public class Posts {
//    public final String blogName;
//
//    private final LinkedHashSet<Post> posts;
//
//    public Posts(Set<Post> posts, String blogName) {
//        this.posts = new LinkedHashSet<>(posts);
//        this.blogName = blogName;
//    }
//
//    public Posts(List<Post> posts, String blogName) {
//        this.posts = new LinkedHashSet<>(posts);
//        this.blogName = blogName;
//    }
//
//    public void printPosts() {
//        for (var post : posts) {
//            post.printPost();
//        }
//    }
//
//    public Set<Post> getPosts() {
//        return Collections.unmodifiableSet(posts);
//    }
//
//    // MARK: - 새로운 아티클 정보에서 과거 아티클 데이터를 뺀 것들을 반환한다.
//    public Posts filterNewposts(Posts newposts) {
//        LinkedHashSet<Post> newpostsSet = new LinkedHashSet<>(newposts.posts);
//        newpostsSet.removeAll(this.posts);
//        return new Posts(newpostsSet, this.blogName);
//    }
//
//    // MARK: - 과거 아티클 데이터와 새로운 아티클 데이터를 합친다.
//    public Posts sumposts(Posts newposts) {
//        LinkedHashSet<Post> newpostsSet = newposts.posts;
//        newpostsSet.addAll(this.posts);
//        return new Posts(newpostsSet, this.blogName);
//    }
//}