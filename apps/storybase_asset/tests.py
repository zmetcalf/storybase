from django.template.defaultfilters import striptags, truncatewords
from django.test import TestCase
from models import HtmlAsset, HtmlAssetTranslation
from embedable_resource import EmbedableResource

class AssetModelTest(TestCase):
    def test_license_name(self):
        asset = HtmlAsset(license='CC BY')
        asset.save()
        translation = HtmlAssetTranslation(title="Test", asset=asset)
        translation.save()
        self.assertEqual(asset.license_name(), 'Attribution Creative Commons')

    def test_string_representation_from_title(self):
        """ Tests that the string representation of an Asset is the Asset's title """
        asset = HtmlAsset()
        asset.save()
        title = "Test Asset Title"
        translation = HtmlAssetTranslation(title=title, asset=asset)
        translation.save()
        self.assertEqual(unicode(asset), asset.title)

    def test_string_representation_from_asset_id(self):
        """ Tests that if a title is not specified, the string representation of the asset is based on the Asset ID """
        asset = HtmlAsset()
        asset.save()
        translation = HtmlAssetTranslation(asset=asset)
        translation.save()
        self.assertEqual(unicode(asset), "Asset %s" % asset.asset_id)

class HtmlAssetModelTest(TestCase):
    def test_string_representation_from_title(self):
        """ Tests that the string representation of an Html Asset is autogenerated from the Body field when no title is present """ 
        asset = HtmlAsset()
        asset.save()
        body = "Eboney Brown's kids range from age one to age nine, so it helps that her daycare center, Early Excellence, is just a short walk from Wyatt-Edison Charter School, where her older kids go. Early Excellence, which welcomes guests with a mural of a white Denver skyline set against a backdrop of blue mountains, serves families from as far away as Thornton and Green Valley Ranch. And many of those families, says Early Excellence director Jennifer Luke, are caught in a cycle of poverty and depend daily on regional transportation. \"I know they can't put a bus on every corner,\" says Luke, who knows many parents who combine public transportation with long walks - year round, no matter the weather."
        translation = HtmlAssetTranslation(body=body, asset=asset)
        translation.save()
        self.assertEqual(unicode(asset), truncatewords(striptags(asset.body), 4))

    def test_display_title_with_no_explicit_title(self):
        """ Tests that the display_title() method returns an automatically
        generated title when an explicit title isn't set

        """
        asset = HtmlAsset()
        asset.save()
        body = "Eboney Brown's kids range from age one to age nine, so it helps that her daycare center, Early Excellence, is just a short walk from Wyatt-Edison Charter School, where her older kids go. Early Excellence, which welcomes guests with a mural of a white Denver skyline set against a backdrop of blue mountains, serves families from as far away as Thornton and Green Valley Ranch. And many of those families, says Early Excellence director Jennifer Luke, are caught in a cycle of poverty and depend daily on regional transportation. \"I know they can't put a bus on every corner,\" says Luke, who knows many parents who combine public transportation with long walks - year round, no matter the weather."
        translation = HtmlAssetTranslation(body=body, asset=asset)
        translation.save()
        self.assertEqual(asset.display_title(),
                         truncatewords(striptags(asset.body), 4))

class EmbedableResourceTest(TestCase):
    def test_get_google_spreadsheet_embed(self):
        url = 'https://docs.google.com/spreadsheet/pub?key=0As2exFJJWyJqdDhBejVfN1RhdDg2b0QtYWR4X2FTZ3c&output=html' 
        expected = "<iframe width='500' height='300' frameborder='0' src='%s&widget=true'></iframe>" % url
        self.assertEqual(EmbedableResource.get_html(url), expected)
