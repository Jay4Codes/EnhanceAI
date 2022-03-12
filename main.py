import cv2
import streamlit as st
import numpy as np
from datetime import date
from streamlit_folium import folium_static
from PIL import Image, ImageEnhance
import pandas as pd
from st_aggrid import AgGrid
import folium

st.set_page_config(
   page_title="Image Editor",
   page_icon="",
   layout="wide",
   initial_sidebar_state="collapsed",
)

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
      <a class="navbar-brand" href="homepage.html"><img src="images/logo.png" alt="logo"></a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="ti-menu text-white"></span>
      </button>
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
rad1 =st.sidebar.radio("Navigation",["Home","Profile", "About-Us"])


#Create two columns with different width
col1, col2 = st.columns( [0.8, 0.2])
with col1:
    st.markdown('<p class="font">Upload your photo here...</p>', unsafe_allow_html=True)


if rad1 == "Home":
    #Add a header and expander in side bar
    st.markdown("""<section class="about section bg-2" id="about">
	<div class="container">
		<div class="row">
			<div class="col-lg-6 align-self-center text-center">
				<!-- Image Content -->
				<div class="image-block">
					<img class="phone-thumb-md" src="images/phones/iphone-feature.png" alt="iphone-feature" class="img-fluid">
				</div>
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

    st.sidebar.markdown('<p class="font"> Image Editor </p>', unsafe_allow_html=True)
    with st.sidebar.expander("About the App"):
        st.write("""
            Use this simple app to convert your favorite photo to a pencil sketch, a grayscale image or an image with blurring effect.  \n  \nThis app was created by Sharone Li as a side project to learn Streamlit and computer vision. Hope you enjoy!
        """)

    #Add file uploader to allow users to upload photos
    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
    #Add 'before' and 'after' columns
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image,width=300)  

        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)

        #Add conditional statements to take the user input values
        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
            filter = st.sidebar.radio('Covert your photo to:', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect'])
            if filter == 'Gray Image':
                    converted_img = np.array(image.convert('RGB'))
                    gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                    st.image(gray_scale, width=300)
            elif filter == 'Black and White':
                    converted_img = np.array(image.convert('RGB'))
                    gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                    slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
                    (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
                    st.image(blackAndWhiteImage, width=300)
            elif filter == 'Pencil Sketch':
                    converted_img = np.array(image.convert('RGB')) 
                    gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                    inv_gray = 255 - gray_scale
                    slider = st.sidebar.slider('Adjust the intensity', 25, 255, 125, step=2)
                    blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
                    sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
                    st.image(sketch, width=300) 
            elif filter == 'Blur Effect':
                    converted_img = np.array(image.convert('RGB'))
                    slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2)
                    converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
                    blur_image = cv2.GaussianBlur(converted_img, (slider,slider), 0, 0)
                    st.image(blur_image, channels='BGR', width=300) 
            else: 
                    st.image(image, width=300)

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
					<h2 class="mb-3">Our Creative Team</h2>
					<p>Demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee idea of
						denouncing pleasure and praising</p>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-lg-3 col-md-6">
				<!-- Team Member -->
<div class="team-member text-center mb-4 mb-lg-0">
	<div class="image">
		<img class="img-fluid" src="images/team/member-one.jpg" alt="team-member">
	</div>
	<div class="name">
		<h5>Johnny Depp</h5>
	</div>
	<div class="position">
		<p>Production Designer</p>
	</div>
	<div class="skill-bar">
		<div class="progress">
		  	<div class="progress-bar" style="width:85%;"></div>
		</div>
		<span>85%</span>
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
	<div class="image">
		<img class="img-fluid" src="images/team/member-two.jpg" alt="team-member">
	</div>
	<div class="name">
		<h5>cristin milioti</h5>
	</div>
	<div class="position">
		<p>UX Researcher</p>
	</div>
	<div class="skill-bar">
		<div class="progress">
		  	<div class="progress-bar" style="width:95%;"></div>
		</div>
		<span>95%</span>
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
	<div class="image">
		<img class="img-fluid" src="images/team/member-three.jpg" alt="team-member">
	</div>
	<div class="name">
		<h5>john doe</h5>
	</div>
	<div class="position">
		<p>Head of Ideas</p>
	</div>
	<div class="skill-bar">
		<div class="progress">
		  	<div class="progress-bar" style="width:80%;"></div>
		</div>
		<span>80%</span>
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
	<div class="image">
		<img class="img-fluid" src="images/team/member-four.jpg" alt="team-member">
	</div>
	<div class="name">
		<h5>mario gotze</h5>
	</div>
	<div class="position">
		<p>UX/UI designer</p>
	</div>
	<div class="skill-bar">
		<div class="progress">
		  	<div class="progress-bar" style="width:75%;"></div>
		</div>
		<span>75%</span>
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
		</div>
	</div>
</section>""", unsafe_allow_html=True)

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
    st.title("Image Editor")

    st.subheader('Locate Us')
    m = folium.Map(location=[19.106790750000002, 72.8414303725908], zoom_start=16)

    # add marker for DJ Sanghvi College Of Engineering
    tooltip = "DJ Sanghvi College Of Engineering"
    folium.Marker(
        [19.106790750000002, 72.8414303725908], popup="DJ Sanghvi College Of Engineering", tooltip=tooltip
    ).add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)

st.markdown("""<footer class="footer-main">
  <div class="container">
    <div class="row">
      <div class="col-lg-6 mr-auto">
        <div class="footer-logo">
          <img src="images/logo.png" alt="footer-logo">
        </div>
        <div class="copyright">
          <p>@2019 Themefisher All Rights Reserved | Design and Developed By : <a href="https://themefisher.com/"
              target="_blank">Themefisher</a>
            <br> Check Our Store for more <a href="https://themefisher.com/free-bootstrap-templates/" target="_blank">Bootstrap Template</a>
          </p>
        </div>
      </div>
      <div class="col-lg-6 text-lg-right">
        <!-- Social Icons -->
        <ul class="social-icons list-inline">
          <li class="list-inline-item">
            <a target="_blank" href="https://facebook.com/themefisher"><i class="text-primary ti-facebook"></i></a>
          </li>
          <li class="list-inline-item">
            <a target="_blank" href="https://twitter.com/themefisher"><i class="text-primary ti-twitter-alt"></i></a>
          </li>
          <li class="list-inline-item">
            <a target="_blank" href="https://github.com/themefisher"><i class="text-primary ti-linkedin"></i></a>
          </li>
          <li class="list-inline-item">
            <a target="_blank" href="https://instagram.com/themefisher"><i class="text-primary ti-instagram"></i></a>
          </li>
        </ul>
        <!-- Footer Links -->
        <ul class="footer-links list-inline">
          <li class="list-inline-item">
            <a class="scrollTo" href="#about">ABOUT</a>
          </li>
          <li class="list-inline-item">
            <a class="scrollTo" href="#team">TEAM</a>
          </li>
          <li class="list-inline-item">
            <a class="scrollTo" href="#contact">CONTACT</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</footer>""", unsafe_allow_html=True)