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

def test_java_valid_1():
    res = detect(test_engines.BASE_SAMPLES["java"], engine="java")
    assert res.candidates

def test_java_valid_2():
    res = detect(test_engines.BASE_SAMPLES["java"], engine="java")
    assert res.candidates

def test_java_valid_3():
    res = detect(test_engines.BASE_SAMPLES["java"], engine="java")
    assert res.candidates

def test_java_valid_4():
    res = detect(test_engines.BASE_SAMPLES["java"], engine="java")
    assert res.candidates

def test_java_valid_5():
    res = detect(test_engines.BASE_SAMPLES["java"], engine="java")
    assert res.candidates

def test_java_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[0]
    res = detect(payload, engine="java")
    assert not res.candidates

def test_java_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[1]
    res = detect(payload, engine="java")
    assert not res.candidates

def test_java_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[2]
    res = detect(payload, engine="java")
    assert not res.candidates

def test_java_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[3]
    res = detect(payload, engine="java")
    assert not res.candidates

def test_java_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[4]
    res = detect(payload, engine="java")
    assert not res.candidates

def test_java_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[5]
    res = detect(payload, engine="java")
    assert not res.candidates

def test_java_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[6]
    res = detect(payload, engine="java")
    assert not res.candidates

def test_java_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[7]
    res = detect(payload, engine="java")
    assert not res.candidates

def test_java_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[8]
    res = detect(payload, engine="java")
    assert not res.candidates

def test_java_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["java"])[9]
    res = detect(payload, engine="java")
    assert not res.candidates


def test_c_valid_1():
    res = detect(test_engines.BASE_SAMPLES["c"], engine="c")
    assert res.candidates

def test_c_valid_2():
    res = detect(test_engines.BASE_SAMPLES["c"], engine="c")
    assert res.candidates

def test_c_valid_3():
    res = detect(test_engines.BASE_SAMPLES["c"], engine="c")
    assert res.candidates

def test_c_valid_4():
    res = detect(test_engines.BASE_SAMPLES["c"], engine="c")
    assert res.candidates

def test_c_valid_5():
    res = detect(test_engines.BASE_SAMPLES["c"], engine="c")
    assert res.candidates

def test_c_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[0]
    res = detect(payload, engine="c")
    assert not res.candidates

def test_c_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[1]
    res = detect(payload, engine="c")
    assert not res.candidates

def test_c_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[2]
    res = detect(payload, engine="c")
    assert not res.candidates

def test_c_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[3]
    res = detect(payload, engine="c")
    assert not res.candidates

def test_c_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[4]
    res = detect(payload, engine="c")
    assert not res.candidates

def test_c_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[5]
    res = detect(payload, engine="c")
    assert not res.candidates

def test_c_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[6]
    res = detect(payload, engine="c")
    assert not res.candidates

def test_c_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[7]
    res = detect(payload, engine="c")
    assert not res.candidates

def test_c_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[8]
    res = detect(payload, engine="c")
    assert not res.candidates

def test_c_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["c"])[9]
    res = detect(payload, engine="c")
    assert not res.candidates


def test_js_valid_1():
    res = detect(test_engines.BASE_SAMPLES["js"], engine="js")
    assert res.candidates

def test_js_valid_2():
    res = detect(test_engines.BASE_SAMPLES["js"], engine="js")
    assert res.candidates

def test_js_valid_3():
    res = detect(test_engines.BASE_SAMPLES["js"], engine="js")
    assert res.candidates

def test_js_valid_4():
    res = detect(test_engines.BASE_SAMPLES["js"], engine="js")
    assert res.candidates

def test_js_valid_5():
    res = detect(test_engines.BASE_SAMPLES["js"], engine="js")
    assert res.candidates

def test_js_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[0]
    res = detect(payload, engine="js")
    assert not res.candidates

def test_js_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[1]
    res = detect(payload, engine="js")
    assert not res.candidates

def test_js_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[2]
    res = detect(payload, engine="js")
    assert not res.candidates

def test_js_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[3]
    res = detect(payload, engine="js")
    assert not res.candidates

def test_js_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[4]
    res = detect(payload, engine="js")
    assert not res.candidates

def test_js_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[5]
    res = detect(payload, engine="js")
    assert not res.candidates

def test_js_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[6]
    res = detect(payload, engine="js")
    assert not res.candidates

def test_js_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[7]
    res = detect(payload, engine="js")
    assert not res.candidates

def test_js_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[8]
    res = detect(payload, engine="js")
    assert not res.candidates

def test_js_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["js"])[9]
    res = detect(payload, engine="js")
    assert not res.candidates


def test_ruby_valid_1():
    res = detect(test_engines.BASE_SAMPLES["ruby"], engine="ruby")
    assert res.candidates

def test_ruby_valid_2():
    res = detect(test_engines.BASE_SAMPLES["ruby"], engine="ruby")
    assert res.candidates

def test_ruby_valid_3():
    res = detect(test_engines.BASE_SAMPLES["ruby"], engine="ruby")
    assert res.candidates

def test_ruby_valid_4():
    res = detect(test_engines.BASE_SAMPLES["ruby"], engine="ruby")
    assert res.candidates

def test_ruby_valid_5():
    res = detect(test_engines.BASE_SAMPLES["ruby"], engine="ruby")
    assert res.candidates

def test_ruby_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[0]
    res = detect(payload, engine="ruby")
    assert not res.candidates

def test_ruby_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[1]
    res = detect(payload, engine="ruby")
    assert not res.candidates

def test_ruby_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[2]
    res = detect(payload, engine="ruby")
    assert not res.candidates

def test_ruby_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[3]
    res = detect(payload, engine="ruby")
    assert not res.candidates

def test_ruby_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[4]
    res = detect(payload, engine="ruby")
    assert not res.candidates

def test_ruby_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[5]
    res = detect(payload, engine="ruby")
    assert not res.candidates

def test_ruby_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[6]
    res = detect(payload, engine="ruby")
    assert not res.candidates

def test_ruby_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[7]
    res = detect(payload, engine="ruby")
    assert not res.candidates

def test_ruby_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[8]
    res = detect(payload, engine="ruby")
    assert not res.candidates

def test_ruby_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["ruby"])[9]
    res = detect(payload, engine="ruby")
    assert not res.candidates


def test_rust_valid_1():
    res = detect(test_engines.BASE_SAMPLES["rust"], engine="rust")
    assert res.candidates

def test_rust_valid_2():
    res = detect(test_engines.BASE_SAMPLES["rust"], engine="rust")
    assert res.candidates

def test_rust_valid_3():
    res = detect(test_engines.BASE_SAMPLES["rust"], engine="rust")
    assert res.candidates

def test_rust_valid_4():
    res = detect(test_engines.BASE_SAMPLES["rust"], engine="rust")
    assert res.candidates

def test_rust_valid_5():
    res = detect(test_engines.BASE_SAMPLES["rust"], engine="rust")
    assert res.candidates

def test_rust_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[0]
    res = detect(payload, engine="rust")
    assert not res.candidates

def test_rust_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[1]
    res = detect(payload, engine="rust")
    assert not res.candidates

def test_rust_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[2]
    res = detect(payload, engine="rust")
    assert not res.candidates

def test_rust_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[3]
    res = detect(payload, engine="rust")
    assert not res.candidates

def test_rust_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[4]
    res = detect(payload, engine="rust")
    assert not res.candidates

def test_rust_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[5]
    res = detect(payload, engine="rust")
    assert not res.candidates

def test_rust_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[6]
    res = detect(payload, engine="rust")
    assert not res.candidates

def test_rust_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[7]
    res = detect(payload, engine="rust")
    assert not res.candidates

def test_rust_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[8]
    res = detect(payload, engine="rust")
    assert not res.candidates

def test_rust_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["rust"])[9]
    res = detect(payload, engine="rust")
    assert not res.candidates


def test_cpp_valid_1():
    res = detect(test_engines.BASE_SAMPLES["cpp"], engine="cpp")
    assert res.candidates

def test_cpp_valid_2():
    res = detect(test_engines.BASE_SAMPLES["cpp"], engine="cpp")
    assert res.candidates

def test_cpp_valid_3():
    res = detect(test_engines.BASE_SAMPLES["cpp"], engine="cpp")
    assert res.candidates

def test_cpp_valid_4():
    res = detect(test_engines.BASE_SAMPLES["cpp"], engine="cpp")
    assert res.candidates

def test_cpp_valid_5():
    res = detect(test_engines.BASE_SAMPLES["cpp"], engine="cpp")
    assert res.candidates

def test_cpp_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[0]
    res = detect(payload, engine="cpp")
    assert not res.candidates

def test_cpp_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[1]
    res = detect(payload, engine="cpp")
    assert not res.candidates

def test_cpp_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[2]
    res = detect(payload, engine="cpp")
    assert not res.candidates

def test_cpp_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[3]
    res = detect(payload, engine="cpp")
    assert not res.candidates

def test_cpp_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[4]
    res = detect(payload, engine="cpp")
    assert not res.candidates

def test_cpp_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[5]
    res = detect(payload, engine="cpp")
    assert not res.candidates

def test_cpp_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[6]
    res = detect(payload, engine="cpp")
    assert not res.candidates

def test_cpp_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[7]
    res = detect(payload, engine="cpp")
    assert not res.candidates

def test_cpp_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[8]
    res = detect(payload, engine="cpp")
    assert not res.candidates

def test_cpp_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["cpp"])[9]
    res = detect(payload, engine="cpp")
    assert not res.candidates


def test_scala_valid_1():
    res = detect(test_engines.BASE_SAMPLES["scala"], engine="scala")
    assert res.candidates

def test_scala_valid_2():
    res = detect(test_engines.BASE_SAMPLES["scala"], engine="scala")
    assert res.candidates

def test_scala_valid_3():
    res = detect(test_engines.BASE_SAMPLES["scala"], engine="scala")
    assert res.candidates

def test_scala_valid_4():
    res = detect(test_engines.BASE_SAMPLES["scala"], engine="scala")
    assert res.candidates

def test_scala_valid_5():
    res = detect(test_engines.BASE_SAMPLES["scala"], engine="scala")
    assert res.candidates

def test_scala_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[0]
    res = detect(payload, engine="scala")
    assert not res.candidates

def test_scala_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[1]
    res = detect(payload, engine="scala")
    assert not res.candidates

def test_scala_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[2]
    res = detect(payload, engine="scala")
    assert not res.candidates

def test_scala_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[3]
    res = detect(payload, engine="scala")
    assert not res.candidates

def test_scala_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[4]
    res = detect(payload, engine="scala")
    assert not res.candidates

def test_scala_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[5]
    res = detect(payload, engine="scala")
    assert not res.candidates

def test_scala_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[6]
    res = detect(payload, engine="scala")
    assert not res.candidates

def test_scala_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[7]
    res = detect(payload, engine="scala")
    assert not res.candidates

def test_scala_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[8]
    res = detect(payload, engine="scala")
    assert not res.candidates

def test_scala_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["scala"])[9]
    res = detect(payload, engine="scala")
    assert not res.candidates


def test_python_valid_1():
    res = detect(test_engines.BASE_SAMPLES["python"], engine="python")
    assert res.candidates

def test_python_valid_2():
    res = detect(test_engines.BASE_SAMPLES["python"], engine="python")
    assert res.candidates

def test_python_valid_3():
    res = detect(test_engines.BASE_SAMPLES["python"], engine="python")
    assert res.candidates

def test_python_valid_4():
    res = detect(test_engines.BASE_SAMPLES["python"], engine="python")
    assert res.candidates

def test_python_valid_5():
    res = detect(test_engines.BASE_SAMPLES["python"], engine="python")
    assert res.candidates

def test_python_invalid_1():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[0]
    res = detect(payload, engine="python")
    assert not res.candidates

def test_python_invalid_2():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[1]
    res = detect(payload, engine="python")
    assert not res.candidates

def test_python_invalid_3():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[2]
    res = detect(payload, engine="python")
    assert not res.candidates

def test_python_invalid_4():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[3]
    res = detect(payload, engine="python")
    assert not res.candidates

def test_python_invalid_5():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[4]
    res = detect(payload, engine="python")
    assert not res.candidates

def test_python_invalid_6():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[5]
    res = detect(payload, engine="python")
    assert not res.candidates

def test_python_invalid_7():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[6]
    res = detect(payload, engine="python")
    assert not res.candidates

def test_python_invalid_8():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[7]
    res = detect(payload, engine="python")
    assert not res.candidates

def test_python_invalid_9():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[8]
    res = detect(payload, engine="python")
    assert not res.candidates

def test_python_invalid_10():
    payload = test_engines._invalid_variants(test_engines.BASE_SAMPLES["python"])[9]
    res = detect(payload, engine="python")
    assert not res.candidates
