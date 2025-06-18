import os

from . import test_engines

import pytest
from probium import detect

def test_exe_valid_1():
    res = detect(test_engines.BASE_SAMPLES["exe"], engine="exe")
    assert res.candidates

def test_exe_valid_2():
    res = detect(test_engines.BASE_SAMPLES["exe"], engine="exe")
    assert res.candidates

def test_exe_valid_3():
    res = detect(test_engines.BASE_SAMPLES["exe"], engine="exe")
    assert res.candidates

def test_exe_valid_4():
    res = detect(test_engines.BASE_SAMPLES["exe"], engine="exe")
    assert res.candidates

def test_exe_valid_5():
    res = detect(test_engines.BASE_SAMPLES["exe"], engine="exe")
    assert res.candidates

def test_exe_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[0]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_exe_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[1]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_exe_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[2]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_exe_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[3]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_exe_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[4]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_exe_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[5]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_exe_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[6]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_exe_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[7]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_exe_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[8]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_exe_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["exe"])[9]
    res = detect(payload, engine="exe")
    assert not res.candidates

def test_image_valid_1():
    res = detect(test_engines.BASE_SAMPLES["image"], engine="image")
    assert res.candidates

def test_image_valid_2():
    res = detect(test_engines.BASE_SAMPLES["image"], engine="image")
    assert res.candidates

def test_image_valid_3():
    res = detect(test_engines.BASE_SAMPLES["image"], engine="image")
    assert res.candidates

def test_image_valid_4():
    res = detect(test_engines.BASE_SAMPLES["image"], engine="image")
    assert res.candidates

def test_image_valid_5():
    res = detect(test_engines.BASE_SAMPLES["image"], engine="image")
    assert res.candidates

def test_image_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[0]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_image_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[1]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_image_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[2]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_image_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[3]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_image_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[4]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_image_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[5]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_image_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[6]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_image_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[7]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_image_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[8]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_image_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["image"])[9]
    res = detect(payload, engine="image")
    assert not res.candidates

def test_mp3_valid_1():
    res = detect(test_engines.BASE_SAMPLES["mp3"], engine="mp3")
    assert res.candidates

def test_mp3_valid_2():
    res = detect(test_engines.BASE_SAMPLES["mp3"], engine="mp3")
    assert res.candidates

def test_mp3_valid_3():
    res = detect(test_engines.BASE_SAMPLES["mp3"], engine="mp3")
    assert res.candidates

def test_mp3_valid_4():
    res = detect(test_engines.BASE_SAMPLES["mp3"], engine="mp3")
    assert res.candidates

def test_mp3_valid_5():
    res = detect(test_engines.BASE_SAMPLES["mp3"], engine="mp3")
    assert res.candidates

def test_mp3_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[0]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_mp3_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[1]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_mp3_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[2]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_mp3_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[3]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_mp3_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[4]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_mp3_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[5]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_mp3_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[6]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_mp3_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[7]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_mp3_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[8]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_mp3_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp3"])[9]
    res = detect(payload, engine="mp3")
    assert not res.candidates

def test_sh_valid_1():
    res = detect(test_engines.BASE_SAMPLES["sh"], engine="sh")
    assert res.candidates

def test_sh_valid_2():
    res = detect(test_engines.BASE_SAMPLES["sh"], engine="sh")
    assert res.candidates

def test_sh_valid_3():
    res = detect(test_engines.BASE_SAMPLES["sh"], engine="sh")
    assert res.candidates

def test_sh_valid_4():
    res = detect(test_engines.BASE_SAMPLES["sh"], engine="sh")
    assert res.candidates

def test_sh_valid_5():
    res = detect(test_engines.BASE_SAMPLES["sh"], engine="sh")
    assert res.candidates

def test_sh_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[0]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_sh_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[1]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_sh_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[2]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_sh_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[3]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_sh_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[4]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_sh_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[5]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_sh_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[6]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_sh_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[7]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_sh_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[8]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_sh_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["sh"])[9]
    res = detect(payload, engine="sh")
    assert not res.candidates

def test_xml_valid_1():
    res = detect(test_engines.BASE_SAMPLES["xml"], engine="xml")
    assert res.candidates

def test_xml_valid_2():
    res = detect(test_engines.BASE_SAMPLES["xml"], engine="xml")
    assert res.candidates

def test_xml_valid_3():
    res = detect(test_engines.BASE_SAMPLES["xml"], engine="xml")
    assert res.candidates

def test_xml_valid_4():
    res = detect(test_engines.BASE_SAMPLES["xml"], engine="xml")
    assert res.candidates

def test_xml_valid_5():
    res = detect(test_engines.BASE_SAMPLES["xml"], engine="xml")
    assert res.candidates

def test_xml_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[0]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_xml_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[1]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_xml_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[2]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_xml_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[3]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_xml_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[4]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_xml_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[5]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_xml_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[6]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_xml_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[7]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_xml_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[8]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_xml_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["xml"])[9]
    res = detect(payload, engine="xml")
    assert not res.candidates

def test_fallback_engine_valid_1():
    res = detect(test_engines.BASE_SAMPLES["fallback-engine"], engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_valid_2():
    res = detect(test_engines.BASE_SAMPLES["fallback-engine"], engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_valid_3():
    res = detect(test_engines.BASE_SAMPLES["fallback-engine"], engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_valid_4():
    res = detect(test_engines.BASE_SAMPLES["fallback-engine"], engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_valid_5():
    res = detect(test_engines.BASE_SAMPLES["fallback-engine"], engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[0]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[1]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[2]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[3]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[4]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[5]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[6]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[7]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[8]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_fallback_engine_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["fallback-engine"])[9]
    res = detect(payload, engine="fallback-engine")
    assert res.candidates

def test_gzip_valid_1():
    res = detect(test_engines.BASE_SAMPLES["gzip"], engine="gzip")
    assert res.candidates

def test_gzip_valid_2():
    res = detect(test_engines.BASE_SAMPLES["gzip"], engine="gzip")
    assert res.candidates

def test_gzip_valid_3():
    res = detect(test_engines.BASE_SAMPLES["gzip"], engine="gzip")
    assert res.candidates

def test_gzip_valid_4():
    res = detect(test_engines.BASE_SAMPLES["gzip"], engine="gzip")
    assert res.candidates

def test_gzip_valid_5():
    res = detect(test_engines.BASE_SAMPLES["gzip"], engine="gzip")
    assert res.candidates

def test_gzip_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[0]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_gzip_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[1]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_gzip_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[2]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_gzip_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[3]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_gzip_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[4]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_gzip_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[5]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_gzip_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[6]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_gzip_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[7]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_gzip_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[8]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_gzip_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["gzip"])[9]
    res = detect(payload, engine="gzip")
    assert not res.candidates

def test_html_valid_1():
    res = detect(test_engines.BASE_SAMPLES["html"], engine="html")
    assert res.candidates

def test_html_valid_2():
    res = detect(test_engines.BASE_SAMPLES["html"], engine="html")
    assert res.candidates

def test_html_valid_3():
    res = detect(test_engines.BASE_SAMPLES["html"], engine="html")
    assert res.candidates

def test_html_valid_4():
    res = detect(test_engines.BASE_SAMPLES["html"], engine="html")
    assert res.candidates

def test_html_valid_5():
    res = detect(test_engines.BASE_SAMPLES["html"], engine="html")
    assert res.candidates

def test_html_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[0]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_html_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[1]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_html_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[2]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_html_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[3]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_html_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[4]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_html_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[5]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_html_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[6]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_html_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[7]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_html_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[8]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_html_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["html"])[9]
    res = detect(payload, engine="html")
    assert not res.candidates

def test_json_valid_1():
    res = detect(test_engines.BASE_SAMPLES["json"], engine="json")
    assert res.candidates

def test_json_valid_2():
    res = detect(test_engines.BASE_SAMPLES["json"], engine="json")
    assert res.candidates

def test_json_valid_3():
    res = detect(test_engines.BASE_SAMPLES["json"], engine="json")
    assert res.candidates

def test_json_valid_4():
    res = detect(test_engines.BASE_SAMPLES["json"], engine="json")
    assert res.candidates

def test_json_valid_5():
    res = detect(test_engines.BASE_SAMPLES["json"], engine="json")
    assert res.candidates

def test_json_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[0]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_json_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[1]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_json_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[2]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_json_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[3]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_json_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[4]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_json_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[5]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_json_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[6]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_json_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[7]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_json_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[8]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_json_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["json"])[9]
    res = detect(payload, engine="json")
    assert not res.candidates

def test_mp4_valid_1():
    res = detect(test_engines.BASE_SAMPLES["mp4"], engine="mp4")
    assert res.candidates

def test_mp4_valid_2():
    res = detect(test_engines.BASE_SAMPLES["mp4"], engine="mp4")
    assert res.candidates

def test_mp4_valid_3():
    res = detect(test_engines.BASE_SAMPLES["mp4"], engine="mp4")
    assert res.candidates

def test_mp4_valid_4():
    res = detect(test_engines.BASE_SAMPLES["mp4"], engine="mp4")
    assert res.candidates

def test_mp4_valid_5():
    res = detect(test_engines.BASE_SAMPLES["mp4"], engine="mp4")
    assert res.candidates

def test_mp4_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[0]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_mp4_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[1]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_mp4_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[2]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_mp4_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[3]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_mp4_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[4]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_mp4_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[5]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_mp4_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[6]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_mp4_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[7]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_mp4_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[8]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_mp4_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["mp4"])[9]
    res = detect(payload, engine="mp4")
    assert not res.candidates

def test_pdf_valid_1():
    res = detect(test_engines.BASE_SAMPLES["pdf"], engine="pdf")
    assert res.candidates

def test_pdf_valid_2():
    res = detect(test_engines.BASE_SAMPLES["pdf"], engine="pdf")
    assert res.candidates

def test_pdf_valid_3():
    res = detect(test_engines.BASE_SAMPLES["pdf"], engine="pdf")
    assert res.candidates

def test_pdf_valid_4():
    res = detect(test_engines.BASE_SAMPLES["pdf"], engine="pdf")
    assert res.candidates

def test_pdf_valid_5():
    res = detect(test_engines.BASE_SAMPLES["pdf"], engine="pdf")
    assert res.candidates

def test_pdf_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[0]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_pdf_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[1]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_pdf_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[2]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_pdf_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[3]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_pdf_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[4]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_pdf_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[5]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_pdf_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[6]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_pdf_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[7]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_pdf_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[8]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_pdf_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["pdf"])[9]
    res = detect(payload, engine="pdf")
    assert not res.candidates

def test_png_valid_1():
    res = detect(test_engines.BASE_SAMPLES["png"], engine="png")
    assert res.candidates

def test_png_valid_2():
    res = detect(test_engines.BASE_SAMPLES["png"], engine="png")
    assert res.candidates

def test_png_valid_3():
    res = detect(test_engines.BASE_SAMPLES["png"], engine="png")
    assert res.candidates

def test_png_valid_4():
    res = detect(test_engines.BASE_SAMPLES["png"], engine="png")
    assert res.candidates

def test_png_valid_5():
    res = detect(test_engines.BASE_SAMPLES["png"], engine="png")
    assert res.candidates

def test_png_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[0]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_png_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[1]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_png_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[2]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_png_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[3]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_png_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[4]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_png_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[5]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_png_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[6]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_png_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[7]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_png_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[8]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_png_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["png"])[9]
    res = detect(payload, engine="png")
    assert not res.candidates

def test_csv_valid_1():
    res = detect(test_engines.BASE_SAMPLES["csv"], engine="csv")
    assert res.candidates

def test_csv_valid_2():
    res = detect(test_engines.BASE_SAMPLES["csv"], engine="csv")
    assert res.candidates

def test_csv_valid_3():
    res = detect(test_engines.BASE_SAMPLES["csv"], engine="csv")
    assert res.candidates

def test_csv_valid_4():
    res = detect(test_engines.BASE_SAMPLES["csv"], engine="csv")
    assert res.candidates

def test_csv_valid_5():
    res = detect(test_engines.BASE_SAMPLES["csv"], engine="csv")
    assert res.candidates

def test_csv_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[0]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_csv_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[1]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_csv_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[2]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_csv_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[3]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_csv_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[4]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_csv_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[5]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_csv_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[6]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_csv_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[7]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_csv_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[8]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_csv_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["csv"])[9]
    res = detect(payload, engine="csv")
    assert not res.candidates

def test_text_valid_1():
    res = detect(test_engines.BASE_SAMPLES["text"], engine="text")
    assert res.candidates

def test_text_valid_2():
    res = detect(test_engines.BASE_SAMPLES["text"], engine="text")
    assert res.candidates

def test_text_valid_3():
    res = detect(test_engines.BASE_SAMPLES["text"], engine="text")
    assert res.candidates

def test_text_valid_4():
    res = detect(test_engines.BASE_SAMPLES["text"], engine="text")
    assert res.candidates

def test_text_valid_5():
    res = detect(test_engines.BASE_SAMPLES["text"], engine="text")
    assert res.candidates

def test_text_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[0]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_text_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[1]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_text_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[2]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_text_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[3]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_text_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[4]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_text_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[5]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_text_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[6]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_text_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[7]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_text_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[8]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_text_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["text"])[9]
    res = detect(payload, engine="text")
    assert not res.candidates

def test_tar_valid_1():
    res = detect(test_engines.BASE_SAMPLES["tar"], engine="tar")
    assert res.candidates

def test_tar_valid_2():
    res = detect(test_engines.BASE_SAMPLES["tar"], engine="tar")
    assert res.candidates

def test_tar_valid_3():
    res = detect(test_engines.BASE_SAMPLES["tar"], engine="tar")
    assert res.candidates

def test_tar_valid_4():
    res = detect(test_engines.BASE_SAMPLES["tar"], engine="tar")
    assert res.candidates

def test_tar_valid_5():
    res = detect(test_engines.BASE_SAMPLES["tar"], engine="tar")
    assert res.candidates

def test_tar_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[0]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_tar_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[1]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_tar_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[2]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_tar_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[3]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_tar_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[4]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_tar_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[5]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_tar_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[6]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_tar_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[7]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_tar_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[8]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_tar_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["tar"])[9]
    res = detect(payload, engine="tar")
    assert not res.candidates

def test_wav_valid_1():
    res = detect(test_engines.BASE_SAMPLES["wav"], engine="wav")
    assert res.candidates

def test_wav_valid_2():
    res = detect(test_engines.BASE_SAMPLES["wav"], engine="wav")
    assert res.candidates

def test_wav_valid_3():
    res = detect(test_engines.BASE_SAMPLES["wav"], engine="wav")
    assert res.candidates

def test_wav_valid_4():
    res = detect(test_engines.BASE_SAMPLES["wav"], engine="wav")
    assert res.candidates

def test_wav_valid_5():
    res = detect(test_engines.BASE_SAMPLES["wav"], engine="wav")
    assert res.candidates

def test_wav_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[0]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_wav_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[1]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_wav_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[2]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_wav_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[3]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_wav_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[4]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_wav_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[5]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_wav_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[6]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_wav_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[7]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_wav_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[8]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_wav_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["wav"])[9]
    res = detect(payload, engine="wav")
    assert not res.candidates

def test_zipoffice_valid_1():
    res = detect(test_engines.BASE_SAMPLES["zipoffice"], engine="zipoffice")
    assert res.candidates

def test_zipoffice_valid_2():
    res = detect(test_engines.BASE_SAMPLES["zipoffice"], engine="zipoffice")
    assert res.candidates

def test_zipoffice_valid_3():
    res = detect(test_engines.BASE_SAMPLES["zipoffice"], engine="zipoffice")
    assert res.candidates

def test_zipoffice_valid_4():
    res = detect(test_engines.BASE_SAMPLES["zipoffice"], engine="zipoffice")
    assert res.candidates

def test_zipoffice_valid_5():
    res = detect(test_engines.BASE_SAMPLES["zipoffice"], engine="zipoffice")
    assert res.candidates

def test_zipoffice_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[0]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_zipoffice_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[1]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_zipoffice_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[2]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_zipoffice_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[3]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_zipoffice_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[4]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_zipoffice_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[5]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_zipoffice_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[6]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_zipoffice_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[7]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_zipoffice_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[8]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_zipoffice_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["zipoffice"])[9]
    res = detect(payload, engine="zipoffice")
    assert not res.candidates

def test_legacyoffice_valid_1():
    res = detect(test_engines.BASE_SAMPLES["legacyoffice"], engine="legacyoffice")
    assert res.candidates

def test_legacyoffice_valid_2():
    res = detect(test_engines.BASE_SAMPLES["legacyoffice"], engine="legacyoffice")
    assert res.candidates

def test_legacyoffice_valid_3():
    res = detect(test_engines.BASE_SAMPLES["legacyoffice"], engine="legacyoffice")
    assert res.candidates

def test_legacyoffice_valid_4():
    res = detect(test_engines.BASE_SAMPLES["legacyoffice"], engine="legacyoffice")
    assert res.candidates

def test_legacyoffice_valid_5():
    res = detect(test_engines.BASE_SAMPLES["legacyoffice"], engine="legacyoffice")
    assert res.candidates

def test_legacyoffice_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[0]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_legacyoffice_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[1]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_legacyoffice_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[2]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_legacyoffice_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[3]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_legacyoffice_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[4]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_legacyoffice_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[5]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_legacyoffice_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[6]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_legacyoffice_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[7]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_legacyoffice_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[8]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_legacyoffice_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["legacyoffice"])[9]
    res = detect(payload, engine="legacyoffice")
    assert not res.candidates

def test_bat_valid_1():
    res = detect(test_engines.BASE_SAMPLES["bat"], engine="bat")
    assert res.candidates

def test_bat_valid_2():
    res = detect(test_engines.BASE_SAMPLES["bat"], engine="bat")
    assert res.candidates

def test_bat_valid_3():
    res = detect(test_engines.BASE_SAMPLES["bat"], engine="bat")
    assert res.candidates

def test_bat_valid_4():
    res = detect(test_engines.BASE_SAMPLES["bat"], engine="bat")
    assert res.candidates

def test_bat_valid_5():
    res = detect(test_engines.BASE_SAMPLES["bat"], engine="bat")
    assert res.candidates

def test_bat_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[0]
    res = detect(payload, engine="bat")
    assert not res.candidates

def test_bat_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[1]
    res = detect(payload, engine="bat")
    assert not res.candidates

def test_bat_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[2]
    res = detect(payload, engine="bat")
    assert not res.candidates

def test_bat_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[3]
    res = detect(payload, engine="bat")
    assert not res.candidates

def test_bat_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[4]
    res = detect(payload, engine="bat")
    assert not res.candidates

def test_bat_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[5]
    res = detect(payload, engine="bat")
    assert not res.candidates

def test_bat_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[6]
    res = detect(payload, engine="bat")
    assert not res.candidates

def test_bat_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[7]
    res = detect(payload, engine="bat")
    assert not res.candidates

def test_bat_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[8]
    res = detect(payload, engine="bat")
    assert not res.candidates

def test_bat_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["bat"])[9]
    res = detect(payload, engine="bat")
    assert not res.candidates

