from turtle import width
from warnings import filters
from chardet import detect
import cv2
from cv2 import transform  
import tensorflow as tf
import time
from patchify import patchify, unpatchify
import streamlit as st
import numpy as np
from datetime import date
from streamlit_folium import folium_static
from PIL import Image, ImageEnhance
from streamlit_cropper import st_cropper
import pandas as pd
from scipy.interpolate import UnivariateSpline
import folium

st.set_page_config(
   page_title="Image Editor",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown(""" 
<style>
/*=== MEDIA QUERY ===*/
@import url("https://fonts.googleapis.com/css?family=Josefin+Sans:300,400,600,700|Open+Sans:400,400i,700");
body {
  font-family: "Open Sans", sans-serif;
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
  font-family: "Open Sans", sans-serif;
  color: #000;
  font-weight: 400;
  line-height: 1;
}

h1 {
  font-size: 60px;
}

h2 {
  font-size: 48px;
}

h3 {
  font-size: 36px;
}

h4 {
  font-size: 30px;
}

h5 {
  font-size: 20px;
}

h6 {
  font-size: 16px;
}

p, li, blockquote, label {
  font-size: 14px;
  letter-spacing: 0;
  line-height: 22px;
  color: #999999;
  margin-bottom: 0;
}

p {
  line-height: 27px;
}

.lead {
  font-size: 1.5rem;
  line-height: 1.5;
}

cite {
  font-size: 14px;
  font-style: normal;
}

.form-control::-webkit-input-placeholder {
  color: #999999;
  font-size: 16px;
}

.app-badge ul li.list-inline-item:not(:last-child) {
  margin-right: 25px;
}

@media (max-width: 768px) {
  .app-badge ul li.list-inline-item:not(:last-child) {
    margin-bottom: 25px;
    margin-right: 0;
  }
}

ul.feature-list {
  margin: 0;
  padding: 0;
}

ul.feature-list li {
  list-style: none;
  margin: 15px 0;
  font-size: 16px;
}

ul.post-tag {
  margin-bottom: 20px;
}

ul.post-tag li {
  font-size: 14px;
}

ul.post-tag li img {
  width: 25px;
  height: 25px;
  border-radius: 100%;
  margin-right: 5px;
}

ul.post-tag li a {
  font-size: 14px;
}

ul.post-tag li:last-child {
  margin-left: 25px;
}

ul.social-icons li a {
  display: block;
  height: 35px;
  width: 35px;
  background: #f8f8f8;
  text-align: center;
  border-radius: 100%;
}

ul.social-icons li a i {
  font-size: 16px;
  line-height: 35px;
}

ul.rating {
  margin-bottom: 0;
}

ul.rating li {
  color: #FFC000;
  font-size: 26px;
}

.shadow, .about .about-block .about-item, .screenshots .screenshot-slider .image img, .counter .counter-item, .team-member, .service .service-box, .founder img, .team-sm .image img, .post-sm, .job-list .block, .privacy .block, .user-login .block .image img, .coming-soon .block .count-down .syotimer-cell {
  box-shadow: 0px 20px 30px 0px rgba(0, 0, 0, 0.05);
}

.transition, .main-nav, .main-nav .navbar-brand {
  transition: .3s ease;
}

.overlay:before {
  content: '';
  background: rgba(125, 113, 211, 0.9);
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

a {
  color: inherit;
  transition: .2s ease;
}

a:focus,
a:hover {
  color: #7d71d3;
  text-decoration: none;
}

.bg-1 {
  background: url(../images/backgrounds/banner-bg.jpg) no-repeat;
  background-size: cover;
}

.bg-2 {
  background: url(../images/backgrounds/elipse-bg.png) no-repeat;
  background-size: cover;
  background-position: center center;
}

.bg-3 {
  background: url(../images/backgrounds/desk-bg.jpg) fixed no-repeat;
  background-size: cover;
}

.bg-banner-2 {
  background: url(../images/backgrounds/banner-bg-two.jpg) no-repeat;
  background-size: cover;
}

.bg-elipse {
  background: url(../images/backgrounds/elipse-bg-three.png) no-repeat;
  background-position: center;
}

.bg-elipse-red {
  background: url(../images/backgrounds/elipse-bg-two.png) no-repeat;
  background-position: center;
}

.bg-elipse-half {
  background: url(../images/backgrounds/elipse-bg-three.png) no-repeat;
  background-position: center;
}

.bg-shape {
  background: url(../images/backgrounds/shape-bg.png) no-repeat;
  background-position: center;
}

.bg-primary-shape {
  background: url(../images/backgrounds/shape-overlay-bg.jpg) no-repeat;
  background-size: cover;
  background-position: center;
}

.bg-shape-two {
  background: url(../images/backgrounds/shape-02-bg.png) no-repeat;
  background-position: center;
}

.text-primary {
  color: #7d71d3 !important;
}

.bg-gray {
  background: #f8f8f8;
}

.bg-blue {
  background: #7d71d3;
}

.bg-coming-soon {
  background: url(../images/background/comming-soon.png) fixed no-repeat;
  background-size: cover;
  background-position: bottom;
}

.section {
  padding: 100px 0;
}

.section-title {
  text-align: center;
  margin-bottom: 85px;
}

.section-title h2 {
  font-size: 48px;
  font-family: "Josefin Sans", sans-serif;
  font-weight: 500;
  margin-bottom: 30px;
}

.section-title p {
  width: 70%;
  margin: 0 auto;
  font-size: 16px;
  line-height: 30px;
}

@media (max-width: 480px) {
  .section-title p {
    width: 100%;
  }
}

.page-title {
  text-align: center;
}

.slick-slide {
  outline: 0;
}

.video {
  position: relative;
}

.video:before {
  border-radius: 3px;
}

.video img {
  width: 100%;
  border-radius: 8px;
}

.video .video-button {
  position: absolute;
  left: 0;
  top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.video .video-box a {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video .video-box a .icon {
  height: 130px;
  width: 130px;
  position: relative;
}

.video .video-box a .icon:before {
  position: absolute;
  content: '';
  height: 100px;
  width: 100px;
  border-radius: 100%;
  background: rgba(125, 113, 211, 0.7);
  position: absolute;
  left: 50%;
  top: 50%;
  -webkit-transform: translate(-50%, -50%);
          transform: translate(-50%, -50%);
}

.video .video-box a .icon:after {
  position: absolute;
  top: 0;
  content: '';
  height: 130px;
  width: 130px;
  border-radius: 100%;
  background: rgba(125, 113, 211, 0.5);
}

.video .video-box a .icon i {
  position: relative;
  left: 50%;
  top: 50%;
  -webkit-transform: translate(-50%, -50%);
          transform: translate(-50%, -50%);
  z-index: 500;
  display: block;
  height: 70px;
  width: 70px;
  font-size: 35px;
  background: #7d71d3;
  border-radius: 100%;
  color: #fff;
  line-height: 70px;
  text-align: center;
}

.video .video-box a iframe {
  width: 100%;
  height: 100%;
}

.form-control {
  background: #fff;
  padding: 20px 20px;
  border: none;
  height: 60px;
  font-size: 14px;
  border-radius: 4px;
}

.form-control:focus {
  border-color: #7d71d3;
  outline: 0;
  box-shadow: none;
}

.input-group {
  box-shadow: 0px 20px 30px 0px rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

.input-group .input-group-text {
  padding-left: 35px;
  padding-right: 35px;
  background: #7d71d3;
  color: #fff;
  cursor: pointer;
}

.form-control::-webkit-input-placeholder {
  color: #999999;
  font-size: 14px;
}

.left {
  overflow: hidden;
}

.left img {
  margin-left: -40px;
}

@media (max-width: 768px) {
  .left img {
    margin-left: 0;
    margin-bottom: 30px;
  }
}

.right {
  overflow: hidden;
}

.right img {
  margin-left: 40px;
}

@media (max-width: 768px) {
  .right img {
    margin-left: 0;
  }
}

.hide-overflow, .service {
  overflow: hidden;
}

.nav-up {
  top: -70px;
}

@media (max-width: 768px) {
  .mb-md-30 {
    margin-bottom: 30px;
  }
}

.btn {
  text-transform: uppercase;
}

.btn-download {
  padding: 10px 25px;
  font-size: 14px;
  background: #232323;
  color: #fff;
  display: flex;
  align-items: center;
  text-align: left;
}

.btn-download i {
  font-size: 40px;
  margin-right: 10px;
}

.btn-download span {
  display: block;
  font-size: 20px;
}

.btn-download:hover {
  color: #fff;
}

.btn-main {
  padding: 25px 45px;
  border-radius: 3px;
  background: #7d71d3;
  color: #fff;
  outline: none;
}

.btn-main:hover {
  color: #fff;
}

.btn-main:focus {
  color: #fff;
  box-shadow: none;
}

.btn-main-rounded {
  letter-spacing: .075em;
  background: #7d71d3;
  color: #fff;
  text-transform: uppercase;
  padding: 15px 40px;
  border-radius: 100px;
}

.btn-main-rounded:hover {
  color: #fff;
}

.btn-main-md {
  padding: 17px 38px;
  border-radius: 3px;
  background: #7d71d3;
  color: #fff;
  outline: none;
}

.btn-main-md:hover {
  color: #fff;
}

.btn-main-md:focus {
  color: #fff;
  box-shadow: none;
}

.btn-main-sm {
  padding: 15px 35px;
  border-radius: 3px;
  background: #7d71d3;
  color: #fff;
  outline: none;
  font-size: 14px;
}

.btn-main-sm:hover {
  color: #fff;
}

.btn-main-sm:focus {
  color: #fff;
  box-shadow: none;
}

.btn-white {
  background: white;
  color: #7d71d3;
}

.btn-rounded-icon {
  border-radius: 100px;
  color: #fff;
  border: 1px solid #fff;
  padding: 13px 50px;
}

.main-nav {
  background: #7d71d3;
  box-shadow: 0px 3px 10px 0px rgba(0, 0, 0, 0.1);
}

.main-nav .navbar-brand {
  padding: 0;
}

.main-nav .navbar-nav .nav-item {
  position: relative;
}

.main-nav .navbar-nav .nav-item .nav-link {
  position: relative;
  text-align: center;
  font-size: 13px;
  text-transform: uppercase;
  color: #fff;
  padding-left: 15px;
  padding-right: 15px;
}

.navbar-toggler:focus, .navbar-toggler:hover {
  outline: none;
}

.large {
  padding-top: 25px;
  padding-bottom: 25px;
}

.small {
  padding-top: 10px;
  padding-bottom: 10px;
}

.footer-main {
  padding: 50px 0;
  background: #7d71d3;
}

@media (max-width: 768px) {
  .footer-main {
    text-align: center;
  }
}

.footer-main .footer-logo {
  margin-bottom: 15px;
}

.footer-main .copyright {
  opacity: .7;
}

.footer-main .copyright p {
  color: #fff;
}

.footer-main .copyright a:hover {
  color: #fff;
}

@media (max-width: 768px) {
  .footer-main ul.social-icons {
    margin-top: 30px;
  }
}

.footer-main ul.footer-links {
  margin-top: 44px;
}

@media (max-width: 768px) {
  .footer-main ul.footer-links {
    margin-top: 20px;
  }
}

.footer-main ul.footer-links li a {
  color: #fff;
  padding: 0 10px;
  display: block;
  opacity: .7;
}

.footer-main ul.footer-links li a:hover {
  opacity: 1;
}

.footer-main ul.footer-links li:last-child a {
  padding-right: 0;
}

.footer-classic {
  background: #fafafa;
  text-align: center;
  padding: 110px 0;
}

.footer-classic ul.social-icons {
  margin-bottom: 30px;
}

@media (max-width: 480px) {
  .footer-classic ul.social-icons li {
    margin-bottom: 10px;
  }
}

.footer-classic ul.social-icons li a {
  padding: 0 20px;
  display: block;
}

.footer-classic ul.social-icons li a i {
  font-size: 25px;
  color: #000;
}

.footer-classic ul.footer-links li a {
  padding: 0 10px;
  display: block;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 14px;
  color: #000;
}

@media (max-width: 768px) {
  .cta-subscribe .image {
    margin-bottom: 30px;
    text-align: center;
  }
}

.cta-subscribe .content {
  margin-left: 25px;
}

@media (max-width: 768px) {
  .cta-subscribe .content {
    text-align: center;
  }
}

.cta-subscribe .content .title {
  margin-bottom: 25px;
}

.cta-subscribe .content .title h2 {
  font-family: "Josefin Sans", sans-serif;
  font-weight: 300;
}

.cta-subscribe .content .description {
  margin-bottom: 40px;
}

.cta-subscribe .content .subscription-tag {
  margin-top: 25px;
}

.cta-subscribe .content .subscription-tag p {
  color: #7d71d3;
  letter-spacing: .1em;
}

.call-to-action-app {
  text-align: center;
}

.call-to-action-app h2, .call-to-action-app p, .call-to-action-app a {
  color: #fff !important;
}

.call-to-action-app p {
  margin-bottom: 60px;
}

.call-to-action-app ul li {
  margin-left: 15px;
}

@media (max-width: 480px) {
  .call-to-action-app ul li {
    margin-left: 0;
    margin-bottom: 10px;
  }
}

.call-to-action-app ul li:first-child {
  margin-left: 0;
}

.call-to-action-app ul li a i {
  font-size: 20px;
  margin-right: 5px;
}

.cta-hire {
  background: #FAFAFA;
}

.cta-hire p {
  width: 65%;
  margin: 0 auto;
}

.cta-hire h2, .cta-hire p {
  margin-bottom: 20px;
}

.cta-community {
  margin: 50px 0;
  padding: 40px 100px;
  display: flex;
}

@media (max-width: 768px) {
  .cta-community {
    flex-wrap: wrap;
    text-align: center;
  }
}

@media (max-width: 400px) {
  .cta-community {
    padding: 20px;
  }
}

.cta-community .content, .cta-community .action-button {
  justify-content: center;
}

.cta-community .action-button {
  align-self: center;
}

@media (max-width: 768px) {
  .cta-community .action-button {
    width: 100%;
    text-align: center;
    margin-top: 20px;
  }
}

.jd-modal .modal-content {
  padding: 25px;
  text-align: left;
  background: #fafafa;
}

.jd-modal .modal-content .modal-header .modal-title {
  color: #000;
}

.jd-modal .modal-content .modal-body .block-2 {
  display: flex;
  margin-bottom: 70px;
}

.jd-modal .modal-content .modal-body .block-2 .title {
  width: 30%;
}

.jd-modal .modal-content .modal-body .block-2 .title p {
  color: #000;
}

.jd-modal .modal-content .modal-body .block-2 .details {
  width: 70%;
}

.jd-modal .modal-content .modal-body .block-2 .details ul {
  padding-left: 0;
  margin: 0;
}

.jd-modal .modal-content .modal-body .block-2 .details ul li {
  list-style: none;
  margin-bottom: 5px;
}

.jd-modal .modal-content .modal-body .block-2 .details ul li span {
  padding-right: 5px;
  color: #000;
}

.jd-modal .modal-content .modal-body .form-title {
  margin-bottom: 30px;
}

.testimonial-slider .client-img {
  background-size: cover;
  background-position: 15px 0;
  background-repeat: no-repeat;
  min-height: 250px;
}

.testimonial-slider .slick-prev {
  left: -100px;
}

.testimonial-slider .slick-next {
  right: -100px;
}

.testimonial-slider .slick-prev, .testimonial-slider .slick-next {
  background: #fff;
  width: 65px;
  height: 55px;
  border-radius: 4px;
}

.testimonial-slider .slick-prev:hover:before, .testimonial-slider .slick-next:hover:before {
  color: #7d71d3;
}

.testimonial-slider .slick-prev:before, .testimonial-slider .slick-next:before {
  color: #999999;
}

.banner {
  padding: 150px 0 100px;
  min-height: 100vh;
}

.banner .content-block.ml-50 {
  margin-left: 50px;
}

@media (max-width: 768px) {
  .banner .content-block.ml-50 {
    margin-left: 30px;
  }
}

@media (max-width: 480px) {
  .banner .content-block.ml-50 {
    margin-left: 0;
  }
}

.banner .content-block h1,
.banner .content-block h5 {
  color: #fff;
}

.banner .content-block h1 {
  line-height: 70px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .06em;
  margin-bottom: 30px;
}

.banner .content-block h5 {
  margin-bottom: 75px;
}

@media (max-width: 480px) {
  .banner .content-block {
    text-align: center;
  }
}

@media (max-width: 480px) {
  .banner .image-block {
    margin-top: 30px;
    text-align: center;
  }
}

.phone-thumb {
  max-height: 550px;
}

.phone-thumb-md {
  max-height: 600px;
}

@media (max-width: 768px) {
  .about .image-block {
    text-align: center;
    margin-bottom: 30px;
  }
}

.about .about-block .about-item {
  background: #fff;
  display: flex;
  padding: 30px;
}

.about .about-block .about-item.active {
  background: #7d71d3;
}

.about .about-block .about-item.active .icon i {
  color: #fff;
}

.about .about-block .about-item.active .content h5,
.about .about-block .about-item.active .content p {
  color: #fff;
}

.about .about-block .about-item .icon {
  width: 50px;
}

.about .about-block .about-item .icon i {
  font-size: 48px;
  color: #7d71d3;
}

.about .about-block .about-item .content {
  margin-left: 30px;
}

.about .about-block .about-item .content h5 {
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 15px;
}

.about .about-block .about-item:not(:last-child) {
  margin-bottom: 30px;
}

.feature .feature-item .icon {
  margin-bottom: 15px;
}

.feature .feature-item .icon i {
  font-size: 48px;
  color: #7d71d3;
}

.feature .feature-item .content h5 {
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 15px;
}

.feature .feature-item:not(:last-child) {
  margin-bottom: 60px;
}

@media (max-width: 768px) {
  .feature .feature-item {
    margin-bottom: 60px;
  }
}

.feature .app-screen {
  margin: 20px 0;
}

.feature .app-screen img {
  max-height: 400px;
}

.promo-video {
  position: relative;
}

.promo-video .section-title h2,
.promo-video .section-title p {
  color: #fff;
}

.screenshots {
  overflow: hidden;
}

.screenshots .screenshot-slider .slick-dots {
  bottom: -60px;
}

.screenshots .screenshot-slider .slick-dots li {
  margin: 0 10px;
}

.screenshots .screenshot-slider .slick-dots li button {
  border: 4px solid #7d71d3;
  border-radius: 100%;
}

.screenshots .screenshot-slider .slick-dots li button:before {
  content: none;
}

.screenshots .screenshot-slider .slick-dots li.slick-active button {
  background: #7d71d3;
}

.pricing-table {
  background: #fff;
  box-shadow: 0px 5px 20px 0px rgba(0, 0, 0, 0.1);
  padding: 50px 0;
  margin-bottom: 80px;
}

.pricing-table.featured .price p {
  color: #ff698d;
}

.pricing-table.featured .action-button .btn-main-rounded {
  background: #ff698d;
}

.pricing-table .title {
  margin-bottom: 30px;
}

.pricing-table .title h5 {
  text-transform: uppercase;
  font-weight: 600;
}

.pricing-table .price {
  margin-bottom: 30px;
}

.pricing-table .price p {
  font-size: 36px;
  font-weight: bold;
  color: #7d71d3;
}

.pricing-table .price p span {
  font-size: 16px;
  font-weight: 400;
}

.pricing-table .action-button {
  margin-top: 30px;
}

.cta-download {
  position: relative;
  padding: 80px 0;
}

.cta-download .image-block {
  position: absolute;
  top: -150px;
  left: 100px;
}

@media (max-width: 992px) {
  .cta-download .image-block {
    display: none;
  }
}

.cta-download .content-block h2,
.cta-download .content-block p {
  color: #fff;
}

.cta-download .content-block h2 {
  font-weight: 500;
  font-family: "Josefin Sans", sans-serif;
  margin-bottom: 30px;
}

.cta-download .content-block p {
  line-height: 30px;
  margin-bottom: 40px;
}

.cta-subscribe h2 {
  font-weight: 500;
  font-family: "Josefin Sans", sans-serif;
}

.counter {
  padding-top: 180px;
}

.counter .counter-item {
  text-align: center;
  background: #7d71d3;
  padding: 40px 0;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .counter .counter-item {
    margin-bottom: 30px;
  }
}

.counter .counter-item h3,
.counter .counter-item p {
  color: #fff;
  text-transform: uppercase;
}

.counter .counter-item h3 {
  margin-bottom: 20px;
  font-weight: 600;
}

.team-member {
  background: #fff;
  padding: 30px;
}

@media (max-width: 768px) {
  .team-member {
    margin-bottom: 40px;
  }
}

.team-member .image {
  margin-bottom: 30px;
}

.team-member .image img {
  border-radius: 100%;
}

.team-member .name h5 {
  font-weight: 600;
  text-transform: uppercase;
}

.team-member .position {
  margin-bottom: 20px;
}

.team-member .skill-bar {
  display: flex;
  margin-bottom: 20px;
}

.team-member .skill-bar .progress {
  width: 80%;
  height: 7px;
  align-self: center;
}

.team-member .skill-bar .progress .progress-bar {
  width: 0;
  background: #7d71d3;
}

.team-member .skill-bar span {
  font-size: 12px;
  margin-left: 15px;
}

.slider {
  padding: 180px 0 300px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.slider .block {
  position: relative;
}

.slider .block h1,
.slider .block h3 {
  color: #fff;
}

.slider .block .download {
  margin-top: 20px;
}

.slider .block .image-content {
  text-align: center;
}

.slider .block .image-content img {
  margin-top: 100px;
  margin-bottom: -200px;
}

.slider:before {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  border-bottom: 290px solid #fff;
  border-left: 2000px solid transparent;
  width: 0;
}

.services .service-block {
  background: #fff;
  padding: 30px 40px;
  margin-bottom: 30px;
  border-radius: 5px;
}

.services .service-block:last-child {
  margin-bottom: 0;
}

@media (max-width: 480px) {
  .services .service-block:last-child {
    margin-bottom: 30px;
  }
}

.services .service-block h3 {
  line-height: 30px;
  text-transform: capitalize;
  font-size: 16px;
  font-weight: 500;
}

.services .service-block i {
  font-size: 30px;
  color: #7d71d3;
  margin-bottom: 15px;
  display: inline-block;
}

.services .service-block p {
  margin-bottom: 0;
  font-size: 14px;
  line-height: 20px;
}

.services .app-preview {
  display: flex;
  justify-content: center !important;
}

.services .app-preview img {
  height: 500px;
  width: auto;
}

@media (max-width: 768px) {
  .services .col-lg-4.m-auto {
    display: none;
  }
}

@media (max-width: 768px) {
  .service .service-thumb {
    width: 80%;
    margin: 0 auto;
  }
}

.service .service-box {
  padding: 20px;
  background: #fff;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .service .service-box {
    width: 80%;
    margin: 0 auto;
  }
}

.service .service-box .service-item {
  text-align: center;
  padding: 10px;
  margin: 20px 0;
}

.service .service-box .service-item i {
  font-size: 20px;
  color: #7d71d3;
  display: inline-block;
  margin-bottom: 10px;
}

.service .service-box .service-item p {
  font-size: 14px;
}

.feature .feature-content h2,
.feature .feature-content p {
  margin-bottom: 25px;
}

@media (max-width: 768px) {
  .feature .feature-content h2,
  .feature .feature-content p {
    text-align: center;
  }
}

@media (max-width: 768px) {
  .feature .testimonial {
    text-align: center;
  }
}

.feature .testimonial p {
  font-family: "Josefin Sans", sans-serif;
  margin-bottom: 10px;
  font-style: italic;
  color: #242424;
}

.feature .testimonial ul.meta li {
  font-size: 12px;
  margin-right: 10px;
}

.feature .testimonial ul.meta li img {
  height: 40px;
  width: 40px;
  border-radius: 100%;
}

@media (max-width: 480px) {
  .app-features .app-feature {
    margin-bottom: 30px;
  }
}

.app-features .app-explore {
  display: flex;
  justify-content: center !important;
  margin-bottom: 40px;
}

.banner-full .image {
  display: flex;
  justify-content: center;
}

.banner-full .image img {
  height: 625px;
}

@media (max-width: 768px) {
  .banner-full .image {
    margin-bottom: 30px;
  }
}

@media (max-width: 768px) {
  .banner-full .block {
    text-align: center;
  }
}

.banner-full .block .logo {
  margin-bottom: 40px;
}

.banner-full .block h1 {
  margin-bottom: 40px;
}

.banner-full .block p {
  font-size: 20px;
  margin-bottom: 50px;
}

.banner-full .block .app {
  margin-bottom: 20px;
}

.video-promo {
  padding: 150px 0;
}

.video-promo .content-block {
  width: 60%;
  margin: 0 auto;
  text-align: center;
}

.video-promo .content-block h2 {
  font-size: 30px;
  color: #fff;
}

.video-promo .content-block p {
  margin-bottom: 30px;
}

.video-promo .content-block a i.video {
  height: 125px;
  width: 125px;
  background: #7d71d3;
  display: inline-block;
  font-size: 40px;
  color: #fff;
  text-align: center;
  line-height: 125px;
  border-radius: 100%;
}

.video-promo .content-block a:focus {
  outline: 0;
}

.founder {
  margin-bottom: 30px;
}

.founder img {
  border-radius: 5px;
  margin-bottom: 25px;
}

.founder h2 {
  font-size: 30px;
  line-height: 30px;
}

.founder cite {
  font-size: 14px;
  font-style: normal;
}

.founder p {
  margin-top: 10px;
  font-size: 14px;
  margin-bottom: 20px;
}

.team-sm {
  margin-bottom: 30px;
}

.team-sm .image {
  position: relative;
  overflow: hidden;
  margin-bottom: 30px;
}

.team-sm .image img {
  border-radius: 5px;
}

.team-sm .image .social-links {
  position: absolute;
  background: #7d71d3;
  left: 0;
  right: 0;
  text-align: center;
  width: calc(100% - 80px);
  margin: 0 40px;
  border-radius: 4px;
  opacity: 0;
  -webkit-transform: translate3d(0, 10px, 0);
          transform: translate3d(0, 10px, 0);
  transition: 0.3s;
  bottom: 20px;
}

.team-sm .image .social-links ul {
  margin-bottom: 0;
}

.team-sm .image .social-links ul li a {
  display: block;
  padding: 15px;
}

.team-sm .image .social-links ul li a i {
  font-size: 20px;
  color: #fff;
}

.team-sm .image:hover .social-links {
  opacity: 1;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}

.team-sm h3 {
  margin-bottom: 0;
}

.team-sm cite {
  font-size: 14px;
  font-style: normal;
}

.team-sm p {
  margin-top: 15px;
}

.featured-article {
  padding: 0 0 50px 0;
}

.featured-article article.featured {
  display: flex;
}

@media (max-width: 768px) {
  .featured-article article.featured {
    flex-wrap: wrap;
  }
}

.featured-article article.featured .image {
  flex-basis: 100%;
  padding: 20px;
}

.featured-article article.featured .image img {
  width: 100%;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .featured-article article.featured .image {
    margin-bottom: 20px;
  }
}

.featured-article article.featured .content {
  margin-left: 30px;
  flex-basis: 100%;
  align-self: center;
}

@media (max-width: 768px) {
  .featured-article article.featured .content {
    text-align: center;
  }
}

.featured-article article.featured .content h2 {
  margin-bottom: 20px;
}

.featured-article article.featured .content h2 a {
  font-size: 30px;
  color: #000;
}

.featured-article article.featured .content h2 a:hover {
  color: #7d71d3;
}

.featured-article article.featured .content p {
  margin-bottom: 25px;
}

.post-sm {
  margin: 10px 0;
  background: #fff;
}

.post-sm .post-thumb {
  overflow: hidden;
}

.post-sm .post-thumb img {
  transition: .3s ease;
}

.post-sm .post-content {
  padding: 30px;
}

.post-sm .post-content .post-title {
  margin-bottom: 15px;
}

.post-sm .post-content .post-title h2 {
  font-size: 20px;
}

.post-sm .post-content .post-title h2 a {
  font-weight: 600;
  text-transform: uppercase;
  line-height: 30px;
  color: #000;
  font-size: 20px;
}

.post-sm .post-content .post-details {
  margin-bottom: 30px;
}

.post-sm .post-content .post-details p {
  line-height: 30px;
}

.post-sm .post-content .excerpts a {
  color: #000;
  letter-spacing: 0.075em;
  font-size: 16px;
  text-transform: uppercase;
  font-weight: 600;
}

.post-sm .post-content .excerpts a span {
  font-weight: 600;
  font-size: 16px;
  color: #000;
  margin-left: 10px;
}

.post-sm .post-content .excerpts a:hover {
  color: #7d71d3;
}

.post-sm .post-content .excerpts a:hover span {
  color: #7d71d3;
}

.blog-single .single-post {
  padding-bottom: 70px;
}

.blog-single .single-post .post-body .feature-image {
  margin-bottom: 30px;
}

.blog-single .single-post .post-body .feature-image img {
  width: 100%;
}

.blog-single .single-post .post-body p {
  margin-bottom: 20px;
}

.blog-single .single-post .post-body .quote {
  padding: 30px 0;
  width: 80%;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .blog-single .single-post .post-body .quote {
    width: 80%;
  }
}

.blog-single .single-post .post-body .quote blockquote {
  color: #000;
  padding: 10px 0 10px 30px;
  text-align: left;
  font-size: 30px;
  line-height: 40px;
  border-left: 6px solid #666666;
}

.blog-single .single-post .post-body .post-image {
  width: 60%;
  margin: 0 auto;
  margin-bottom: 20px;
}

.blog-single .about-author h2 {
  padding-bottom: 15px;
  border-bottom: 1px solid #cccccc;
  margin-bottom: 30px;
  font-size: 30px;
}

@media (max-width: 480px) {
  .blog-single .about-author h2 {
    text-align: center;
  }
}

@media (max-width: 480px) {
  .blog-single .about-author .media {
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .blog-single .about-author .media .image {
    flex-grow: 1;
    width: 100%;
    display: flex;
    justify-content: center;
  }
}

.blog-single .about-author .media .image img {
  width: 150px;
  height: 150px;
  border-radius: 100%;
}

.blog-single .about-author .media .media-body {
  margin-left: 40px;
}

@media (max-width: 480px) {
  .blog-single .about-author .media .media-body {
    flex-grow: 1;
    width: 100%;
    text-align: center;
    margin-left: 0;
    margin-top: 20px;
  }
}

.blog-single .about-author .media .media-body p {
  margin-bottom: 15px;
}

.related-articles .title {
  margin-bottom: 20px;
}

.related-articles .title h2 {
  font-size: 30px;
}

.pagination-nav {
  display: flex;
  justify-content: center;
}

.pagination-nav ul.pagination {
  padding-top: 30px;
}

.pagination-nav ul.pagination li {
  margin-right: 10px;
}

.pagination-nav ul.pagination li a {
  border-radius: 3px;
  padding: 0;
  height: 50px;
  width: 50px;
  line-height: 50px;
  text-align: center;
  border-color: transparent;
  box-shadow: 0px 1px 3px 0px rgba(0, 0, 0, 0.1);
  color: #999999;
  transition: .3s ease-in;
}

.pagination-nav ul.pagination li a:hover {
  background-color: #7d71d3;
  color: #fff;
  border-color: transparent;
}

.pagination-nav ul.pagination .active a {
  background-color: #7d71d3;
  color: #fff;
  border-color: transparent;
}

@media (max-width: 480px) {
  .about .content {
    text-align: center;
  }
}

.about .content h2 {
  margin-bottom: 20px;
  text-transform: capitalize;
}

.about .about-slider .item {
  padding: 20px;
}

.about .about-slider .owl-dots .owl-dot:hover span {
  background: #7d71d3;
}

.about .about-slider .owl-dots .owl-dot.active span {
  background: #7d71d3;
}

.create-stories .block img {
  width: 100%;
  margin-bottom: 20px;
}

.create-stories .block h3 {
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .create-stories .block {
    margin-bottom: 30px;
  }
}

.quotes .quote-slider h2 {
  font-size: 50px;
}

.quotes .quote-slider cite {
  margin-left: 150px;
  font-style: normal;
}

.clients {
  padding: 50px 0;
}

.clients h3 {
  margin-bottom: 30px;
}

.clients .client-slider .owl-stage {
  display: flex;
  align-items: center;
}

.investors .block {
  margin-bottom: 30px;
}

.investors .block .image {
  margin-bottom: 20px;
}

.investors .block .image img {
  width: 100%;
  border-radius: 8px;
}

.investors .block h3 {
  margin-bottom: 0;
  line-height: 1;
}

.investors .block p {
  font-size: 14px;
}

.error-page {
  position: fixed;
  height: 100%;
  width: 100%;
}

.error-page .center {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.error-page .center .block h1 {
  font-size: 200px;
  font-weight: 400;
  line-height: 266px;
  font-family: "Josefin Sans", sans-serif;
}

.error-page .center .block p {
  margin-bottom: 50px;
}

.career-featured .block {
  display: flex;
}

@media (max-width: 768px) {
  .career-featured .block {
    flex-wrap: wrap;
  }
}

.career-featured .block .content {
  flex-basis: 100%;
  align-self: center;
}

@media (max-width: 768px) {
  .career-featured .block .content {
    flex-grow: 1;
    width: 100%;
    margin-bottom: 30px;
    text-align: center;
  }
}

.career-featured .block .content h2 {
  margin-bottom: 30px;
}

.career-featured .block .video {
  justify-content: center;
  align-self: center;
  flex-basis: 100%;
  margin-left: 10px;
}

@media (max-width: 768px) {
  .career-featured .block .video {
    flex-grow: 1;
    width: 100%;
  }
}

.company-fun-facts h2 {
  margin-bottom: 60px;
}

.company-fun-facts .fun-fact {
  margin-bottom: 20px;
  text-align: center;
}

.company-fun-facts .fun-fact i {
  font-size: 25px;
  display: inline-block;
  margin-bottom: 10px;
  line-height: 60px;
  height: 60px;
  width: 60px;
  border: 1px solid #000;
  border-radius: 100%;
}

.gallery .image {
  cursor: pointer;
}

.job-list .block {
  padding: 50px 80px;
  background: #fff;
}

.job-list .block h2 {
  margin-bottom: 60px;
  font-size: 30px;
}

.job-list .block .job {
  padding: 50px 10px;
  border-top: 1px solid #cccccc;
  display: flex;
}

.job-list .block .job:last-child {
  border-bottom: 1px solid #cccccc;
}

@media (max-width: 480px) {
  .job-list .block .job {
    flex-wrap: wrap;
  }
}

.job-list .block .job .content {
  flex-basis: 100%;
}

@media (max-width: 480px) {
  .job-list .block .job .content {
    width: 100%;
    flex-grow: 1;
    text-align: center;
    margin-bottom: 30px;
  }
}

.job-list .block .job .content h3 {
  margin-bottom: 0;
}

.job-list .block .job .apply-button {
  flex-basis: 100%;
  align-self: center;
  text-align: right;
}

@media (max-width: 480px) {
  .job-list .block .job .apply-button {
    width: 100%;
    flex-grow: 1;
    text-align: center;
  }
}

.faq .block {
  padding: 50px;
}

@media (max-width: 480px) {
  .faq .block {
    padding: 30px;
  }
}

.faq .block .faq-item {
  margin-bottom: 40px;
}

.faq .block .faq-item .faq-item-title {
  margin-bottom: 30px;
}

.faq .block .faq-item .faq-item-title h2 {
  font-size: 30px;
  border-bottom: 1px solid #cccccc;
}

.faq .block .faq-item .faq-item-title:last-child {
  margin-bottom: 0;
}

.faq .block .faq-item .item .item-link {
  position: relative;
  padding: 10px 0 10px 18px;
}

.faq .block .faq-item .item .item-link a {
  font-size: 20px;
  color: #000;
}

.faq .block .faq-item .item .item-link a span {
  margin-right: 5px;
}

.faq .block .faq-item .item .item-link:before {
  font-family: themefisher-font;
  content: "\f3d0";
  position: absolute;
  left: 0;
  font-weight: 600;
}

.faq .block .faq-item .item .accordion-block {
  background: #fafafa;
  margin-left: 18px;
}

.faq .block .faq-item .item .accordion-block p {
  padding: 20px;
}

.privacy .privacy-nav {
  position: -webkit-sticky;
  position: sticky;
  top: 15px;
  background: #fafafa;
  padding: 30px 0;
  display: flex;
  justify-content: center;
}

.privacy .privacy-nav ul {
  padding-left: 0;
  margin-bottom: 0;
}

.privacy .privacy-nav ul li {
  list-style: none;
}

.privacy .privacy-nav ul li a {
  font-size: 20px;
  color: #000;
  padding: 10px 0;
  display: block;
}

@media (max-width: 768px) {
  .privacy .privacy-nav ul li a {
    font-size: 16px;
    padding: 5px 0;
  }
}

@media (max-width: 768px) {
  .privacy .privacy-nav {
    margin-bottom: 30px;
  }
}

.privacy .block {
  background: #fff;
  padding: 40px 50px;
}

.privacy .block .policy-item {
  padding-bottom: 40px;
}

.privacy .block .policy-item .title {
  margin-bottom: 20px;
}

.privacy .block .policy-item .title h3 {
  border-bottom: 1px solid #cccccc;
  padding-bottom: 15px;
}

.privacy .block .policy-item .policy-details p {
  margin-bottom: 40px;
}

.user-login {
  height: 100%;
  width: 100%;
}

.user-login .block {
  display: flex;
}

@media (max-width: 768px) {
  .user-login .block {
    flex-wrap: wrap;
  }
}

.user-login .block .image {
  flex-basis: 100%;
  margin-right: 40px;
}

@media (max-width: 768px) {
  .user-login .block .image {
    flex-grow: 1;
    text-align: center;
    margin-bottom: 30px;
    margin-right: 0;
  }
}

.user-login .block .image img {
  border-radius: 8px;
}

.user-login .block .content {
  flex-basis: 100%;
  align-self: center;
  padding: 50px;
  border: 1px solid #cccccc;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .user-login .block .content {
    flex-grow: 1;
  }
}

.user-login .block .content .logo {
  margin-bottom: 80px;
}

@media (max-width: 992px) {
  .user-login .block .content .logo {
    margin-bottom: 40px;
  }
}

.user-login .block .content .title-text {
  margin-bottom: 35px;
}

.user-login .block .content .title-text h3 {
  padding-bottom: 20px;
  border-bottom: 1px solid #cccccc;
}

.user-login .block .content .new-acount {
  margin-top: 20px;
}

.user-login .block .content .new-acount p, .user-login .block .content .new-acount a {
  font-size: 14px;
}

.user-login .block .content .new-acount p a {
  color: #000;
}

.coming-soon {
  color: #000;
  padding: 120px 0;
  height: 100vh;
}

@media (max-width: 992px) {
  .coming-soon {
    padding: 80px 0;
  }
}

.coming-soon .block h3 {
  color: #999999;
}

.coming-soon .block .count-down {
  margin-top: 70px;
}

@media (max-width: 768px) {
  .coming-soon .block .count-down {
    margin-top: 40px;
  }
}

.coming-soon .block .count-down .syotimer-cell {
  min-width: 200px;
  padding: 45px 0;
  margin-right: 30px;
  margin-bottom: 20px;
  background: #fff;
  display: inline-block;
}

.coming-soon .block .count-down .syotimer-cell .syotimer-cell__value {
  font-size: 65px;
  line-height: 80px;
  text-align: center;
  position: relative;
  font-weight: bold;
}

.coming-soon .block .count-down .syotimer-cell .syotimer-cell__unit {
  font-size: 20px;
  color: #6c6c6c;
  text-transform: uppercase;
  font-weight: normal;
}

.address .block .address-block {
  text-align: center;
}

.address .block .address-block .icon {
  margin-bottom: 25px;
  display: flex;
  justify-content: center;
}

.address .block .address-block .icon i {
  display: block;
  height: 100px;
  width: 100px;
  background: #fafafa;
  border-radius: 100%;
  font-size: 45px;
  text-align: center;
  line-height: 100px;
}

.address .google-map {
  position: relative;
}

.address .google-map #googleMap {
  height: 400px;
  width: 100%;
}

/*# sourceMappingURL=maps/style.css.map */
</style>
""", unsafe_allow_html=True)
 
st.markdown("""
<nav class="navbar main-nav fixed-top navbar-expand-lg large">
  <div class="container">
      <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <a class="nav-link scrollTo" href="#home">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link scrollTo" href="#about">About</a>
        </li>
        <li class="nav-item">
          <a class="nav-link scrollTo" href="#feature">Features</a>
        </li>
        <li class="nav-item">
          <a class="nav-link scrollTo" href="#pricing">Pricing</a>
        </li>
        <li class="nav-item">
          <a class="nav-link scrollTo" href="#team">Team</a>
        </li>
        <li class="nav-item">
          <a class="nav-link scrollTo" href="#contact">Contact</a>
        </li>
      </ul>
      </div>
  </div>
</nav>""", unsafe_allow_html=True)

st.sidebar.title('Image Editor')
rad1 =st.sidebar.radio("Navigation",["Home", 'Editor', "EnhanceAI", "Transform", "Profile", "About-Us"])

st.sidebar.markdown('<p class="font"> Image Editor </p>', unsafe_allow_html=True)
with st.sidebar.expander("About the App"):
  st.write("""
     Use this simple app to convert your favorite photo to a pencil sketch, a grayscale image or an image with blurring effect.  \n  \nThis app was created by Team Reinforcers. Hope you enjoy!
    """)

if rad1 == "Home":
    st.image('../images/landing.png', width=1000)
    
    st.markdown("""
    <style>
.macbook {
  width: 150px;
  height: 96px;
  position: absolute;
  left: 50%;
  top: 50%;
  margin: -75px 0 0 -48px;
  perspective: 500px;
}
.shadow {
  position: absolute;
  width: 60px;
  height: 0px;
  left: 40px;
  top: 160px;
  transform: rotateX(80deg) rotateY(0deg) rotateZ(0deg);
  box-shadow: 0 0 60px 40px rgba(0,0,0,0.3);
  animation: shadow infinite 7s ease;
}
.inner {
  z-index: 20;
  position: absolute;
  width: 150px;
  height: 96px;
  left: 0;
  top: 0;
  transform-style: preserve-3d;
  transform:rotateX(-20deg) rotateY(0deg) rotateZ(0deg);
  animation: rotate infinite 7s ease;
}
.screen {
  width: 150px;
  height: 96px;
  position: absolute;
  left: 0;
  bottom: 0;
  border-radius: 7px;
  background: #ddd;
  transform-style: preserve-3d;
  transform-origin: 50% 93px;
  transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
  animation: lid-screen infinite 7s ease;
  background-image: linear-gradient(45deg, rgba(0,0,0,0.34) 0%,rgba(0,0,0,0) 100%);
  background-position: left bottom;
  background-size: 300px 300px;
  box-shadow: inset 0 3px 7px rgba(255,255,255,0.5);
}
.screen .logo {
  position: absolute;
  width: 20px;
  height: 24px;
  left: 50%;
  top: 50%;
  margin: -12px 0 0 -10px;
  transform: rotateY(180deg) translateZ(0.1px);
}
.screen .face-one {
  width: 150px;
  height: 96px;
  position: absolute;
  left: 0;
  bottom: 0;
  border-radius: 7px;
  background: #d3d3d3;
  transform: translateZ(2px);
  background-image: linear-gradient(45deg,rgba(0,0,0,0.24) 0%,rgba(0,0,0,0) 100%);
}
.screen .face-one .camera {
  width: 3px;
  height: 3px;
  border-radius: 100%;
  background: #000;
  position: absolute;
  left: 50%;
  top: 4px;
  margin-left: -1.5px;
}
.screen .face-one .display {
  width: 130px;
  height: 74px;
  margin: 10px;
  background: url("https://upload.wikimedia.org/wikipedia/en/9/98/MacOS_Monterey_Desktop.png") no-repeat center center #000;
  background-size: 100% 100%;
  border-radius: 1px;
  position: relative;
  box-shadow: inset 0 0 2px rgba(0,0,0,1);
}
.screen .face-one .display .shade {
  position: absolute;
  left: 0;
  top: 0;
  width: 130px;
  height: 74px;
  background: linear-gradient(-135deg, rgba(255,255,255,0) 0%,rgba(255,255,255,0.1) 47%,rgba(255,255,255,0) 48%);
  animation: screen-shade infinite 7s ease;
  background-size: 300px 200px;
  background-position: 0px 0px;
}
.screen .face-one span {
  position: absolute;
  top: 85px;
  left: 57px;
  font-size: 6px;
  color: #666
}

.body {
  width: 150px;
  height: 96px;
  position: absolute;
  left: 0;
  bottom: 0;
  border-radius: 7px;
  background: #cbcbcb;
  transform-style: preserve-3d;
  transform-origin: 50% bottom;
  transform: rotateX(-90deg);
  animation: lid-body infinite 7s ease;
  background-image: linear-gradient(45deg, rgba(0,0,0,0.24) 0%,rgba(0,0,0,0) 100%);
}
.body .face-one {
  width: 150px;
  height: 96px;
  position: absolute;
  left: 0;
  bottom: 0;
  border-radius: 7px;
  transform-style: preserve-3d;
  background: #dfdfdf;
  animation: lid-keyboard-area infinite 7s ease;
  transform: translateZ(-2px);
  background-image: linear-gradient(30deg, rgba(0,0,0,0.24) 0%,rgba(0,0,0,0) 100%);
}
.body .touchpad {
  width: 40px;
  height: 31px;
  position: absolute;
  left: 50%;
  top: 50%;
  border-radius: 4px;
  margin: -44px 0 0 -18px;
  background: #cdcdcd;
  background-image: linear-gradient(30deg, rgba(0,0,0,0.24) 0%,rgba(0,0,0,0) 100%);
  box-shadow: inset 0 0 3px #888;
}
.body .keyboard {
width: 130px;
height: 45px;
position: absolute;
left: 7px;
top: 41px;
border-radius: 4px;
transform-style: preserve-3d;
background: #cdcdcd;
background-image: linear-gradient(30deg, rgba(0,0,0,0.24) 0%,rgba(0,0,0,0) 100%);
box-shadow: inset 0 0 3px #777;
padding: 0 0 0 2px;
}
.keyboard .key {
  width: 6px;
  height: 6px;
  background: #444;
  float: left;
  margin: 1px;
  transform: translateZ(-2px);
  border-radius: 2px;
  box-shadow: 0 -2px 0 #222;
  animation: keys infinite 7s ease;
}
.key.space {
  width: 45px;
}
.key.f {
  height: 3px;
}
.body .pad {
  width: 5px;
  height: 5px;
  background: #333;
  border-radius: 100%;
  position: absolute;
}
.pad.one {
  left: 20px;
  top: 20px;
}
.pad.two {
  right: 20px;
  top: 20px;
}
.pad.three {
  right: 20px;
  bottom: 20px;
}
.pad.four {
  left: 20px;
  bottom: 20px;
}

@keyframes rotate {
  0% {
    transform: rotateX(-20deg) rotateY(0deg) rotateZ(0deg);
  }
  5% {
    transform: rotateX(-20deg) rotateY(-20deg) rotateZ(0deg);
  }
  20% {
    transform: rotateX(30deg) rotateY(200deg) rotateZ(0deg);
  }
  25% {
    transform: rotateX(-60deg) rotateY(150deg) rotateZ(0deg);
  }
  60% {
    transform: rotateX(-20deg) rotateY(130deg) rotateZ(0deg);
  }
  65% {
    transform: rotateX(-20deg) rotateY(120deg) rotateZ(0deg);
  }
  80% {
    transform: rotateX(-20deg) rotateY(375deg) rotateZ(0deg);
  }
  85% {
    transform: rotateX(-20deg) rotateY(357deg) rotateZ(0deg);
  }
  87% {
    transform: rotateX(-20deg) rotateY(360deg) rotateZ(0deg);
  }
  100% {
    transform: rotateX(-20deg) rotateY(360deg) rotateZ(0deg);
  }
}

@keyframes lid-screen {
  0% {
    transform: rotateX(0deg);
    background-position: left bottom;
  }
  5% {
    transform: rotateX(50deg);
    background-position: left bottom;
  }
  20% {
    transform: rotateX(-90deg);
    background-position: -150px top;
  }
  25% {
    transform: rotateX(15deg);
    background-position: left bottom;
  }
  30% {
    transform: rotateX(-5deg);
    background-position: right top;
  }
  38% {
    transform: rotateX(5deg);
    background-position: right top;
  }
  48% {
    transform: rotateX(0deg);
    background-position: right top;
  }
  90% {
    transform: rotateX(0deg);
    background-position: right top;
  }
  100% {
    transform: rotateX(0deg);
    background-position: right center;
  }
}

@keyframes lid-body {
  0% {
    transform: rotateX(-90deg);
    
  }
  50% {
    transform: rotateX(-90deg);
    
  }
  100% {
    transform: rotateX(-90deg);
    
  }
}

@keyframes lid-keyboard-area {
  0% {
     background-color: #dfdfdf;
  }
  50% {
    background-color: #bbb;
  }
  100% {
    background-color: #dfdfdf;
  }
}
@keyframes screen-shade {
  0% {
    background-position: -20px 0px;
  }
  5% {
    background-position: -40px 0px;
  }
  20% {
    background-position: 200px 0;
  }
  50% {
    background-position: -200px 0;
  }
  80% {
    background-position: 0px 0px;
  }
  85% {
    background-position: -30px 0;
  }
  90% {
    background-position: -20px 0;
  }
  100% {
    background-position: -20px 0px;
  }
}
@keyframes keys {
  0% {
    box-shadow: 0 -2px 0 #222;
  }
  5% {
    box-shadow: 1 -1px 0 #222;
  }
  20% {
    box-shadow: -1px 1px 0 #222;
  }
  25% {
    box-shadow: -1px 1px 0 #222;
  }
  60% {
    box-shadow: -1px 1px 0 #222;
  }
  80% {
    box-shadow: 0 -2px 0 #222;
  }
  85% {
    box-shadow: 0 -2px 0 #222;
  }
  87% {
    box-shadow: 0 -2px 0 #222;
  }
  100% {
    box-shadow: 0 -2px 0 #222;
  }
}
@keyframes shadow {
  0% {
    transform: rotateX(80deg) rotateY(0deg) rotateZ(0deg);
    box-shadow: 0 0 60px 40px rgba(0,0,0,0.3);
  }
  5% {
    transform: rotateX(80deg) rotateY(10deg) rotateZ(0deg);
    box-shadow: 0 0 60px 40px rgba(0,0,0,0.3);
  }
  20% {
    transform: rotateX(30deg) rotateY(-20deg) rotateZ(-20deg);
    box-shadow: 0 0 50px 30px rgba(0,0,0,0.3);
  }
  25% {
    transform: rotateX(80deg) rotateY(-20deg) rotateZ(50deg);
    box-shadow: 0 0 35px 15px rgba(0,0,0,0.1);
  }
  60% {
    transform: rotateX(80deg) rotateY(0deg) rotateZ(-50deg) translateX(30px);
    box-shadow: 0 0 60px 40px rgba(0,0,0,0.3);
  }
  100% {
    box-shadow: 0 0 60px 40px rgba(0,0,0,0.3);
  }
}
.links {
  position: absolute;
  right: 20px;
  bottom: 20px;
}
.links a {
  color : #555;
  margin-left: 10px;
  text-decoration: none;
}
</style>
<div class="macbook">
  <div class="inner">
    <div class="screen">
      <div class="face-one">
        <div class="camera"></div>
        <div class="display">
          <div class="shade"></div>
        </div>
        <span>MacBook Air</span>
      </div>
      <img src="http://www.clker.com/cliparts/i/s/H/f/4/T/apple-logo-white.svg" class="logo" />
    </div>
    <div class="body">
      <div class="face-one">
        <div class="touchpad">
        </div>
        <div class="keyboard">
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key space"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
          <div class="key f"></div>
        </div>
      </div>
      <div class="pad one"></div>
      <div class="pad two"></div>
      <div class="pad three"></div>
      <div class="pad four"></div>
    </div>
  </div>
  <div class="shadow"></div>
</div>""", unsafe_allow_html=True)
    #Add a header and expander in side bar
    st.markdown("""<section class="about section bg-2" id="about">
	<div class="container">
		<div class="row">
			</div>
			<div class="col-lg-6 col-md-10 m-md-auto align-self-center ml-auto">
				<div class="about-block">
					<!-- About 01 -->
					<div class="about-item">
						<div class="icon">
							<i class="ti-palette"></i>
						</div>
						<div class="content">
							<h5>Creative Design</h5>
							<p>But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born
								and I will give you a complete accounta</p>
						</div>
					</div>
					<!-- About 02 -->
					<div class="about-item active">
						<div class="icon">
							<i class="ti-panel"></i>
						</div>
						<div class="content">
							<h5>Easy to Use</h5>
							<p>But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born
								and I will give you a complete accounta</p>
						</div>
					</div>
					<!-- About 03 -->
					<div class="about-item">
						<div class="icon">
							<i class="ti-vector"></i>
						</div>
						<div class="content">
							<h5>Best User Experience</h5>
							<p>But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born
								and I will give you a complete accounta</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>""", unsafe_allow_html=True)

    st.markdown("""<section class="pricing section bg-shape" id="pricing">
	<div class="container">
		<div class="row">
			<div class="col-12">
				<div class="section-title mb-4">
					<h2 class="mb-3">Choose Your Subscription Plan</h2>
					<p>Demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee idea of
						denouncing pleasure and praising</p>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-lg-4 col-md-6">
				<!-- Pricing Table -->
<div class="pricing-table text-center">	
	<!-- Title -->
	<div class="title">	
		<h5>Free</h5>
	</div>
	<!-- Price Tag -->
	<div class="price">	
		<p>$0<span>/month</span></p>
	</div>
	<!-- Features -->
	<ul class="feature-list">
		<li>Android App</li>
		<li>One time payment</li>
		<li>Build & Publish</li>
		<li>Life time support</li>
	</ul>
	<!-- Take Action -->
	<div class="action-button">
		<a href="" class="btn btn-main-rounded">Start Now</a>
	</div>
</div>
			</div>
			<div class="col-lg-4 col-md-6">
				<!-- Pricing Table -->
<div class="pricing-table featured text-center">	
	<!-- Title -->
	<div class="title">	
		<h5>Basic</h5>
	</div>
	<!-- Price Tag -->
	<div class="price">	
		<p>$19<span>/month</span></p>
	</div>
	<!-- Features -->
	<ul class="feature-list">
		<li>Android App</li>
		<li>One time payment</li>
		<li>Build & Publish</li>
		<li>Life time support</li>
	</ul>
	<!-- Take Action -->
	<div class="action-button">
		<a href="" class="btn btn-main-rounded">Start Now</a>
	</div>
</div>
			</div>
			<div class="col-lg-4 col-md-6 m-md-auto">
				<!-- Pricing Table -->
<div class="pricing-table text-center">	
	<!-- Title -->
	<div class="title">	
		<h5>Advance</h5>
	</div>
	<!-- Price Tag -->
	<div class="price">	
		<p>$99<span>/month</span></p>
	</div>
	<!-- Features -->
	<ul class="feature-list">
		<li>Android App</li>
		<li>One time payment</li>
		<li>Build & Publish</li>
		<li>Life time support</li>
	</ul>
	<!-- Take Action -->
	<div class="action-button">
		<a href="" class="btn btn-main-rounded">Start Now</a>
	</div>
</div>
			</div>
		</div>
	</div>
</section>""", unsafe_allow_html=True)

    st.markdown("""<section class="section team bg-shape-two" id="team">
	<div class="container">
		<div class="row">
			<div class="col-12">
				<div class="section-title mb-4">
					<h2 class="mb-3">Our Team</h2>
					<p>Meet the amazing team of brilliant, dynamic individuals who bring to you an amazing and powerful application to satisy all your needs related to the domain.</p>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-lg-3 col-md-6">
				<!-- Team Member -->
<div class="team-member text-center mb-4 mb-lg-0">
	<div class="name">
		<h5>Aaryan Kangte</h5>
	</div>
	<div class="position">
		<p>Computer Vision</p>
	</div>
	 <div class="skill-bar">
	 	<div class="progress">
	 	  	<div class="progress-bar" style="width:100%;"></div>
	 	</div>
	 	<span>100%</span>
	 </div>
	<ul class="social-icons list-inline">
		<li class="list-inline-item">
			<a href="https://github.com/Aaryan562"><i class="ti-Github"></i></a>
		</li>
		<li class="list-inline-item">
			<a href="https://www.linkedin.com/in/aaryan-kangte-096686225/"><i class="ti-Linkedin-alt"></i></a>
		</li>
		<li class="list-inline-item">
			<a href=""><i class="ti-lTwitter"></i></a>
		</li>
		<li class="list-inline-item">
			<a href=""><i class="ti-instagram"></i></a>
		</li>
	</ul>
</div>
			</div>
			<div class="col-lg-3 col-md-6">
				<!-- Team Member -->
<div class="team-member text-center mb-4 mb-lg-0">
	<div class="name">
		<h5>Arihant Sheth</h5>
	</div>
	<div class="position">
		<p>Deep Learning</p>
	</div>
	 <div class="skill-bar">
	 	<div class="progress">
	 	  	<div class="progress-bar" style="width:100%;"></div>
	 	</div>
	 	<span>100%</span>
	 </div>
	<ul class="social-icons list-inline">
		<li class="list-inline-item">
			<a href=""><i class="ti-facebook"></i></a>
		</li>
		<li class="list-inline-item">
			<a href=""><i class="ti-twitter-alt"></i></a>
		</li>
		<li class="list-inline-item">
			<a href=""><i class="ti-linkedin"></i></a>
		</li>
		<li class="list-inline-item">
			<a href=""><i class="ti-instagram"></i></a>
		</li>
	</ul>
</div>
			</div>
			<div class="col-lg-3 col-md-6">
				<!-- Team Member -->
<div class="team-member text-center mb-4 mb-lg-0">
	 <div class="name">
		<h5>Himanshu Kakwani</h5>
	</div>
	<div class="position">
		<p>Frontend developer</p>
	</div>
	 <div class="skill-bar">
	 	<div class="progress">
	 	  	<div class="progress-bar" style="width:100%;"></div>
	 	</div>
	 	<span>100%</span>
	 </div>
	<ul class="social-icons list-inline">
		<li class="list-inline-item">
			<a href="https://github.com/blueheisenberg69"><i class="ti-Github"></i></a>
		</li>
		<li class="list-inline-item">
			<a href="https://www.linkedin.com/in/himanshu-kakwani-054b71227/"><i class="ti-Linkedin-alt"></i></a>
		</li>
		<li class="list-inline-item">
			<a href=""><i class="ti-linkedin"></i></a>
		</li>
		<li class="list-inline-item">
			<a href=""><i class="ti-instagram"></i></a>
		</li>
	</ul>
</div>
			</div>
			<div class="col-lg-3 col-md-6">
				<!-- Team Member -->
<div class="team-member text-center mb-4 mb-lg-0">
	<div class="name">
		<h5>Jay Jain</h5>
	</div>
	<div class="position">
		<p>Dackend developer</p>
	</div>
	<div class="skill-bar">
		<div class="progress">
		  	<div class="progress-bar" style="width:100%;"></div>
		</div>
		<span>100%</span>
	</div>
	<ul class="social-icons list-inline">
		<li class="list-inline-item">
			<a href="https://github.com/Jay4Codes"><i class="ti-Github"></i></a>
		</li>
		<li class="list-inline-item">
			<a href="https://www.linkedin.com/in/jay-jain-a9bb12200/"><i class="ti-Linkedin-alt"></i></a>
		</li>
		<li class="list-inline-item">
			<a href=""><i class="ti-linkedin"></i></a>
		</li>
		<li class="list-inline-item">
			<a href=""><i class="ti-instagram"></i></a>
		</li>
	</ul>
</div>
			</div>
		</div>
	</div>
</section>""", unsafe_allow_html=True)


if rad1 == "Editor":
    #Add file uploader to allow users to upload photos
    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image,width=400)  

        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
            filter = st.sidebar.radio('Covert your photo to:', ['Original','Black and White', 'Pencil Sketch', 'Sharpen', 'Sepia', 'HDR', 'Smoothen', 'Blur Effect', 'Invert', 'Summer', 'Winter']) #Add the filter in the sidebar
            if filter == 'Gray Image':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                st.image(gray_scale, width=400)
            elif filter == 'Black and White':
                    converted_img = np.array(image.convert('RGB'))
                    gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                    slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
                    (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
                    st.image(blackAndWhiteImage, width=400)
            elif filter == 'Pencil Sketch':
                    converted_img = np.array(image.convert('RGB')) 
                    gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                    inv_gray = 255 - gray_scale
                    slider = st.sidebar.slider('Adjust the intensity', 25, 255, 125, step=2)
                    blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
                    sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
                    st.image(sketch, width=400) 
            elif filter == 'Blur Effect':
                    converted_img = np.array(image.convert('RGB'))
                    slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2)
                    converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
                    blur_image = cv2.GaussianBlur(converted_img, (slider,slider), 0, 0)
                    st.image(blur_image, channels='BGR', width=400)
            elif filter == 'Invert':
                    converted_img = np.array(image.convert('RGB'))
                    inv = cv2.bitwise_not(converted_img)
                    st.image(inv, width=400)
            elif filter == 'Sharpen':
                    converted_img = np.array(image.convert('RGB'))
                    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
                    img_sharpen = cv2.filter2D(converted_img, -1, kernel)
                    st.image(img_sharpen, width=400)
            elif filter == 'Sepia':
                    converted_img = np.array(image.convert('RGB'))
                    img_sepia = np.array(converted_img, dtype=np.float64) # converting to float to prevent loss
                    img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                                        [0.349, 0.686, 0.168],
                                                        [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
                    img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
                    img_sepia = np.array(img_sepia, dtype=np.uint8)
                    st.image(img_sepia, channels='BGR', width=400)
            elif filter == 'Summer':
                    converted_img = np.array(image.convert('RGB'))
                    def LookupTable(x, y):
                      spline = UnivariateSpline(x, y)
                      return spline(range(256))


                    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
                    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
                    blue_channel, green_channel,red_channel  = cv2.split(converted_img)
                    red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
                    blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
                    sum= cv2.merge((blue_channel, green_channel, red_channel ))
                    st.image(sum, channels='BGR', width=400)
            elif filter == 'Winter':
                    def LookupTable(x, y):
                      spline = UnivariateSpline(x, y)
                      return spline(range(256))
                    converted_img = np.array(image.convert('RGB'))
                    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
                    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
                    blue_channel, green_channel,red_channel = cv2.split(converted_img)
                    red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
                    blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
                    win= cv2.merge((blue_channel, green_channel, red_channel))
                    st.image(win, channels='BGR', width=400)
            elif filter == 'HDR':
                    converted_img = np.array(image.convert('RGB'))
                    hdr = cv2.detailEnhance(converted_img, sigma_s=12, sigma_r=0.15)
                    st.image(hdr, width=400)
            elif filter == 'Smoothen':
                    converted_img = np.array(image.convert('RGB'))
                    s_value=100
                    r_value=0.2
                    shade_factor=0.1
                    smooth=cv2.edgePreservingFilter(converted_img,cv2.RECURS_FILTER,s_value,r_value)
                    st.image(smooth, width=400)
            else: 
                    st.image(image, width=400)

if rad1 == "Image-Processing":
  st.header("Image Processing")
  detect_img = st.file_uploader(label='Upload a file', type=['png', 'jpg'])

  def photo():
    st.header("Thresholding, Edge Detection and Contours")
        
    if st.button('See Original Image'):
      original = detect_img
      st.image(original, use_column_width=True)
            
    image = detect_img
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    x = st.slider('Change Threshold value',min_value = 50,max_value = 255)
    ret,thresh1 = cv2.threshold(image,x,255,cv2.THRESH_BINARY)
    thresh1 = thresh1.astype(np.float64)
    st.image(thresh1, use_column_width=True,clamp = True)
        
    st.text("Bar Chart of the image")
    histr = cv2.calcHist([image],[0],None,[256],[0,256])
    st.bar_chart(histr)
        
    st.text("Press the button below to view Canny Edge Detection Technique")
    if st.button('Canny Edge Detector'):
      image = detect_img
      edges = cv2.Canny(image,50,300)
      cv2.imwrite('edges.jpg',edges)
      st.image(edges,use_column_width=True,clamp=True)
          
    y = st.slider('Change Value to increase or decrease contours',min_value = 50,max_value = 255)     
        
    if st.button('Contours'):
      im = detect_img
              
      imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
      ret,thresh = cv2.threshold(imgray,y,255,0)
      image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
      img = cv2.drawContours(im, contours, -1, (0,255,0), 3)
    
            
      st.image(thresh, use_column_width=True, clamp = True)
      st.image(img, use_column_width=True, clamp = True)
      

  def face_detection():
    
    st.header("Face Detection using haarcascade")
    
    if st.button('See Original Image'):
        
        original = detect_img
        st.image(original, use_column_width=True)
    
    
    image2 = detect_img
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(image2)
    print(f"{len(faces)} faces detected in the image.")
    for x, y, width, height in faces:
        cv2.rectangle(image2, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
    
    cv2.imwrite("faces.jpg", image2)
    
    st.image(image2, use_column_width=True,clamp = True)

  def object_detection():
    
    st.header('Object Detection')
    st.subheader("Object Detection is done using different haarcascade files.")
    img = detect_img
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    
    clock = cv2.CascadeClassifier('haarcascade_wallclock.xml')  
    found = clock.detectMultiScale(img_gray, minSize =(20, 20)) 
    amount_found = len(found)
    st.text("Detecting a clock from an image")
    if amount_found != 0:  
        for (x, y, width, height) in found:
          cv2.rectangle(img_rgb, (x, y),  
                          (x + height, y + width),  
                          (0, 255, 0), 5) 
    st.image(img_rgb, use_column_width=True,clamp = True)
    st.text("Detecting eyes from an image")
    
    image = detect_img
    img_gray_ = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    img_rgb_ = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        
    eye = cv2.CascadeClassifier('haarcascade_eye.xml')  
    found = eye.detectMultiScale(img_gray_,  
                                       minSize =(20, 20)) 
    amount_found_ = len(found)
        
    if amount_found_ != 0:  
        for (x, y, width, height) in found:
          cv2.rectangle(img_rgb_, (x, y),  
                              (x + height, y + width),  
                              (0, 255, 0), 5) 
        st.image(img_rgb_, use_column_width=True,clamp = True)



  def main():
      
    selected_box = st.sidebar.selectbox(
      'Choose one of the following',
      ('Image Processing', 'Face Detection', 'Object Detection')
      )
      
    if selected_box == 'Image Processing':
        photo()
    if selected_box == 'Face Detection':
        face_detection()
    if selected_box == 'Object Detection':
        object_detection()

  main()


if rad1 == "EnhanceAI":

  from glob import glob  #
  # Importing required dependencies from MIRNet
  from mirnet.inference import Inferer
  from mirnet.utils import plot_result
  import time

  start = time.time()
  inferer = Inferer()

  img_test = st.file_uploader(label='Upload a file', type=['png', 'jpg'])
  # inferer.download_weights('1sUlRD5MTRKKGxtqyYDpTv7T3jOW6aVAL')
  if img_test is not None:
    inferer.build_model(num_rrg=3, num_mrb=2, channels=64, weights_path=r'C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor\low-light-image-enhancing\MIRNet\low_light_weights_best.h5')
    inferer.model.save('mirnet-saved-model')

    

    original_image, output_image = inferer.infer(img_test)
    print(time.time() - start)
    col1, col2 = st.columns( [0.5, 0.5])
    with col1:
        st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
        st.image(original_image, width=500) 

    with col2:
        st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
        st.image(output_image,  width=500) 


if rad1 == "Transform":
  # Upload an image and set some options for demo purposes
  st.header("Image Transform")
  img_file = st.file_uploader(label='Upload a file', type=['png', 'jpg'])
  realtime_update = st.checkbox(label="Update in Real Time", value=True)
  box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
  aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
  aspect_dict = {
      "1:1": (1, 1),
      "16:9": (16, 9),
      "4:3": (4, 3),
      "2:3": (2, 3),
      "Free": None
  }
  aspect_ratio = aspect_dict[aspect_choice]

  if img_file:
      img = Image.open(img_file)
      if not realtime_update:
          st.write("Double click to save crop")
      # Get a cropped image from the frontend
      cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                  aspect_ratio=aspect_ratio)
      
      # Manipulate cropped image at will
      st.write("Preview")
      _ = cropped_img.thumbnail((150,150))
      st.image(cropped_img)

if rad1 == "Profile":
    st.title("Your Profile")

    col1 , col2 = st.columns(2)

    rad2 =st.radio("Profile",["Sign-Up","Sign-In"])


    if rad2 == "Sign-Up":

        st.title("Registration Form")



        col1 , col2 = st.columns(2)

        fname = col1.text_input("First Name",value = "first name")

        lname = col2.text_input("Second Name")

        col3 , col4 = st.columns([3,1])

        email = col3.text_input("Email ID")

        phone = col4.text_input("Mob number")

        col5 ,col6 ,col7  = st.columns(3)

        username = col5.text_input("Username")

        password =col6.text_input("Password", type = "password")

        col7.text_input("Repeat Password" , type = "password")

        but1,but2,but3 = st.columns([1,4,1])

        agree  = but1.checkbox("I Agree")

        if but3.button("Submit"):
            if agree:  
                st.subheader("Additional Details")

                address = st.text_area("Tell Us Something About You")
                st.write(address)

                st.date_input("Enter your birth-date")

                v1 = st.radio("Gender",["Male","Female","Others"],index = 1)

                st.write(v1)

                st.slider("age",min_value = 18,max_value=60,value = 30,step = 2)

                img = st.file_uploader("Upload your profile picture")
                if img is not None:
                    st.image(img)

            else:
                st.warning("Please Check the T&C box")

    if rad2 == "Sign-In":
        col1 , col2 = st.columns(2)

        username = col1.text_input("Username")

        password =col2.text_input("Password", type = "password")

        but1,but2,but3 = st.columns([1,4,1])

        agree  = but1.checkbox("I Agree")

        if but3.button("Submit"):
            
            if agree:  
                st.subheader("Additional Details")

                address = st.text_area("Tell Us Something About You")
                st.write(address)

                st.date_input("Enter your birth-date")

                v1 = st.radio("Gender",["Male","Female","Others"],index = 1)

                st.write(v1)

                st.slider("age",min_value = 18,max_value=60,value = 30,step = 2)

                img = st.file_uploader("Upload your profile picture")
                if img is not None:
                    st.image(img)
            else:
                st.warning("Please Check the T&C box")

if rad1 == "About-Us": 
    st.image("../images/logo.png")
    st.subheader('Locate Us')
    m = folium.Map(location=[19.106790750000002, 72.8414303725908], zoom_start=16)

    # add marker for DJ Sanghvi College Of Engineering
    tooltip = "DJ Sanghvi College Of Engineering"
    folium.Marker(
        [19.106790750000002, 72.8414303725908], popup="DJ Sanghvi College Of Engineering", tooltip=tooltip
    ).add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)