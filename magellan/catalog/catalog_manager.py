# coding=utf-8
"""
This module contains wrapper functions for the catalog.
"""
import logging

import pandas as pd
import six

import magellan.utils.catalog_helper as ch
from magellan.catalog.catalog import Catalog

logger = logging.getLogger(__name__)


def get_property(data_frame, property_name):
    """
    Gets a property (with the given property name) for a pandas DataFrame from
    the Catalog.

    Args:
        data_frame (DataFrame): Dataframe for which the property should be
            retrieved.
        property_name (str): Name of the property that should be retrieved.

    Returns:
        A pandas object (typically a string or a pandas DataFrame depending
        on the property name) is returned.

    Raises:
        AssertionError: If the object is not of type pandas DataFrame.
        AssertionError: If the property name is not of type string.
        KeyError: If the DataFrame information is not present in the catalog.
        KeyError: If the requested property for the DataFrame is not present
            in the catalog.
    """
    # Validate input parameters

    # # The input object should be of type pandas DataFrame
    if not isinstance(data_frame, pd.DataFrame):
        logger.error('Input object is not of type pandas DataFrame')
        raise AssertionError('Input object is not of type pandas DataFrame')

    # # The property name should be of type string
    if not isinstance(property_name, six.string_types):
        logger.error('Property name is not of type string')
        raise AssertionError('Property name is not of type string')

    # Get the catalog instance, this is imported here because this object
    # used to validate the presence of a DataFrame in the catalog, and the
    # presence of requested metadata in the catalog.
    catalog = Catalog.Instance()

    # Check for the present of input DataFrame in the catalog.
    if not catalog.is_df_info_present_in_catalog(data_frame):
        logger.error('Dataframe information is not present in the catalog')
        raise KeyError('Dataframe information is not present in the catalog')

    # Check if the requested property is present in the catalog.
    if not catalog.is_property_present_for_df(data_frame, property_name):
        logger.error(
            'Requested metadata ( %s ) for the given dataframe is not '
            'present in the catalog', property_name)
        raise KeyError(
            'Requested metadata ( %s ) for the given dataframe is not '
            'present in the catalog', property_name)

    # Return the requested property for the input DataFrame
    return catalog.get_property(data_frame, property_name)


def set_property(data_frame, property_name, property_value):
    """
    Sets a property (with the given property name) for a pandas DataFrame in
    the Catalog.

    Args:
        data_frame (DataFrame): DataFrame for which the property must  be set.
        property_name (str): Name of the property to be set.
        property_value (object): Value of the property to be set. This is
            typically a string (such as key) or pandas DataFrame (such as
            ltable, rtable).

    Returns:
        A boolean value of True is returned if the update was successful.

    Raises:
        AssertionError: If the input object is not of type pandas DataFrame.
        AssertionError: If the property name is not of type string.

    Note:
        If the input DataFrame is not present in the catalog, this function
        will create an entry in the catalog and set the given property.

    """
    # Validate input parameters

    # # The input object is expected to be of type pandas DataFrame
    if not isinstance(data_frame, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    # # The property name is expected to be of type string.
    if not isinstance(property_name, six.string_types):
        logger.error('Property name is not of type string')
        raise AssertionError('Property name is not of type string')


    catalog = Catalog.Instance()

    # Check if the DataFrame information is present in the catalog. If the
    # information is not present, then initialize an entry for that DataFrame
    #  in the catalog.
    if not catalog.is_df_info_present_in_catalog(data_frame):
        catalog.init_properties(data_frame)

    # Set the property in the catalog, and relay the return value from the
    # underlying catalog object's function. The return value is typically
    # True if the update was successful.
    return catalog.set_property(data_frame, property_name, property_value)


def init_properties(data_frame):
    """
    Initializes properties for a pandas DataFrame in the catalog.

    Specifically, this function creates an entry in the catalog and sets its
    properties to empty.

    Args:
        data_frame (DataFrame): DataFrame for which the properties must be
            initialized.

    Returns:
        A boolean value of True is returned if the initialization was
        successful.

    """
    # Validate input parameters

    # # Input object is expected to be of type pandas DataFrame
    if not isinstance(data_frame, pd.DataFrame):
        logger.error('Input object is not of type pandas DataFrame')
        raise AssertionError('Input object is not of type pandas DataFrame')


    catalog = Catalog.Instance()

    # Initialize the property in the catalog.
    # Relay the return value from the underlying catalog object's function.
    # The return value is typically True if the initialization was successful
    return catalog.init_properties(data_frame)


def get_all_properties(data_frame):
    """
    Gets all the properties for a pandas DataFrame object from the catalog.

    Args:
        data_frame (DataFrame): DataFrame for which the properties must be
            retrieved.

    Returns:
        A dictionary containing properties for the input pandas DataFrame.

    Raises:
        AttributeError: If the input object is not of type pandas DataFrame.
        KeyError: If the information about DataFrame is not present in the
            catalog.


    """
    # Validate input parameters
    # # The input object is expected to be of type DataFrame
    if not isinstance(data_frame, pd.DataFrame):
        logger.error('Input object is not of type pandas DataFrame')
        raise AssertionError('Input object is not of type pandas DataFrame')

    catalog = Catalog.Instance()

    # Check if the DataFrame information is present in the catalog. If not
    # raise an error.
    if not catalog.is_df_info_present_in_catalog(data_frame):
        logger.error('Dataframe information is not present in the catalog')
        raise KeyError('Dataframe information is not present in the catalog')

    # Retrieve the properties for the DataFrame from the catalog and return
    # it back to the user.
    return catalog.get_all_properties(data_frame)


def del_property(data_frame, property_name):
    """
    Delete a property for a pandas DataFrame from the catalog.

    Args:
        data_frame (DataFrame): Input DataFrame for which a property must be
            deleted from the catalog.
        property_name (str): Name of the property that should be deleted.

    Returns:
        A boolean value of True is returned if the deletion was successful.

    Raises:
        AssertionError: If the object is not of type pandas DataFrame.
        AssertionError: If the property name is not of type string.
        KeyError: If the DataFrame information is not present in the catalog.
        KeyError: If the requested property for the DataFrame is not present
            in the catalog.
    """
    # Validate input parameters

    # # The input object should be of type pandas DataFrame
    if not isinstance(data_frame, pd.DataFrame):
        logger.error('Input object is not of type pandas DataFrame')
        raise AssertionError('Input object is not of type pandas DataFrame')

    # # The input property name is expected to be of type string
    if not isinstance(property_name, six.string_types):
        logger.error('Property name is not of type string')
        raise AssertionError('Property name is not of type string')

    catalog = Catalog.Instance()

    # Check if the DataFrame information is present in the catalog, if not
    # raise an error.
    if not catalog.is_df_info_present_in_catalog(data_frame):
        logger.error('DataFrame information is not present in the catalog')
        raise KeyError('DataFrame information is not present in the catalog')

    # Check if the requested property name to be deleted  is present for the
    # DataFrame in the catalog, if not raise an error.
    if not catalog.is_property_present_for_df(data_frame, property_name):
        logger.error('Requested metadata ( %s ) for the given DataFrame is '
                     'not present in the catalog', property_name)
        raise KeyError('Requested metadata ( %s ) for the given DataFrame is '
                       'not present in the catalog', property_name)

    # Delete the property using the underlying catalog object and relay the
    # return value. Typically the return value is True if the deletion was
    # successful
    return catalog.del_property(data_frame, property_name)


def del_all_properties(data_frame):
    """
    Delete all properties for a DataFrame from the catalog.

    Args:
        data_frame (DataFrame): Input DataFrame for which all the properties
            must be deleted from the catalog.

    Returns:
        A boolean of True is returned if the deletion was successful
        from the catalog.

    Raises:
        AssertionError: If the input object is not of type pandas DataFrame.
        KeyError: If the DataFrame information is not present in the catalog.

    Note:
        This method's functionality is not as same as init_properties. Here
        the DataFrame's entry will be removed from the catalog,
        but init_properties will add (if the DataFrame is not present in the
        catalog) and initialize its properties to an empty object (
        specifically, an empty python dictionary).
    """
    # Validations of input parameters
    # # The input object is expected to be of type pandas DataFrame
    if not isinstance(data_frame, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    catalog = Catalog.Instance()

    # Check if the DataFrame is present in the catalog. If not, raise an error
    if not catalog.is_df_info_present_in_catalog(data_frame):
        logger.error('Dataframe information is not present in the catalog')
        raise KeyError('Dataframe information is not present in the catalog')

    # Call the underlying catalog object's function to delete the properties
    # and relay its return value
    return catalog.del_all_properties(data_frame)


def get_catalog():
    """
    Get Catalog information.


    Returns:
        Catalog information in a dictionary format.

    """
    catalog = Catalog.Instance()
    return catalog.get_catalog()


def del_catalog():
    """
    Delete catalog information

    Returns:
        status (bool). Returns True if the deletion was successful.
    """
    catalog = Catalog.Instance()
    return catalog.del_catalog()


def is_catalog_empty():
    """
    Check if the catalog is empty

    Returns:
        result (bool). Returns True if the catalog is empty, else returns False.

    """
    catalog = Catalog.Instance()
    return catalog.is_catalog_empty()


def is_dfinfo_present(df):
    """
    Check if the dataframe information is present in the catalog

    Args:
        df (pandas dataframe): Input dataframe

    Returns:
        result (bool). Returns True if the dataframe information is present in the catalog, else returns False

    Raises:
        AttributeError: If the input dataframe is null

    """
    catalog = Catalog.Instance()
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    return catalog.is_df_info_present_in_catalog(df)


def is_property_present_for_df(df, name):
    """
    Check if the property is present for the dataframe

    Args:
        df (pandas dataframe): Input dataframe
        name (str): Property name

    Returns:
        result (bool). Returns True if the property is present for the input dataframe

    Raises:
        AttributeError: If the input dataframe is null
        KeyError: If the dataframe is not present in the catalog

    """
    catalog = Catalog.Instance()
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    if catalog.is_df_info_present_in_catalog(df) is False:
        logger.error('Dataframe information is not present in the catalog')
        raise KeyError('Dataframe information is not present in the catalog')

    return catalog.is_property_present_for_df(df, name)


def get_catalog_len():
    """
    Get the number of entries in the catalog

    Returns:
        length (int) of the catalog

    """
    catalog = Catalog.Instance()
    return catalog.get_catalog_len()


def set_properties(df, prop_dict, replace=True):
    """
    Set properties for a dataframe in the catalog
    Args:
        df (pandas dataframe): Input dataframe
        prop_dict (dict): Property dictionary with keys as property names and values as python objects
        replace (bool): Flag to indicate whether the input properties can replace the properties in the catalog

    Returns:
        status (bool). Returns True if the setting of properties was successful

    Notes:
        The function is intended to set all the properties in the catalog with the given
        property dictionary.
          The replace flag is just a check where the properties will be not be disturbed
          if they exist already in the
          catalog

    """
    catalog = Catalog.Instance()
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    if not isinstance(prop_dict, dict):
        logger.error('The properties should be of type python dictionary')
        raise AssertionError(
            'The properties should be of type python dictionary')

    if catalog.is_df_info_present_in_catalog(df) and replace is False:
        logger.warning(
            'Properties already exists for df ( %s ). Not replacing it' % str(
                id(df)))
        return False

    if not catalog.is_df_info_present_in_catalog(df):
        catalog.init_properties(df)

    # for k, v in prop_dict.iteritems():
    for k, v in six.iteritems(prop_dict):
        catalog.set_property(df, k, v)
    return True


def has_property(df, prop):
    catalog = Catalog.Instance()
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    if not isinstance(prop, six.string_types):
        logger.error('Property name is not of type string')
        raise AssertionError('Property name is not of type string')

    if not is_dfinfo_present(df):
        logger.error('Dataframe is not in the catalog')
        raise KeyError('Dataframe is not in the catalog')

    p = get_all_properties(df)
    # return p.has_key(prop)
    return prop in p


def copy_properties(src, tar, update=True):
    """
    Copy properties from one dataframe to another
    Args:
        src (pandas dataframe): Dataframe from which the properties to be copied from
        tar (pandas dataframe): Dataframe to which the properties to be copied
        update (bool): Flag to indicate whether the source properties can replace
        the tart properties

    Returns:
        status (bool). Returns True if the copying was successful

    Notes:
        This function internally calls set_properties and get_all_properties


    """
    # copy catalog information from src to tar
    catalog = Catalog.Instance()
    if not isinstance(src, pd.DataFrame):
        logger.error('Input object (src) is not of type pandas data frame')
        raise AssertionError(
            'Input object (src) is not of type pandas data frame')

    if not isinstance(tar, pd.DataFrame):
        logger.error('Input object (tar) is not of type pandas data frame')
        raise AssertionError(
            'Input object (tar) is not of type pandas data frame')

    if catalog.is_df_info_present_in_catalog(src) is False:
        logger.error(
            'Dataframe information (src) is not present in the catalog')
        raise KeyError(
            'Dataframe information (src) is not present in the catalog')

    metadata = catalog.get_all_properties(src)
    return set_properties(tar, metadata,
                          update)  # this initializes tar in the catalog.


# key related methods
def get_key(df):
    """
    Get the key attribute for a dataframe

    Args:
        df (pandas dataframe): Dataframe for which the key must be retrieved

    Returns:
        key (str)

    """
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    return get_property(df, 'key')


def set_key(df, key):
    """
    Set the key attribute for a dataframe

    Args:
        df (pandas dataframe): Dataframe for which the key must be set
        key (str): Key attribute in the dataframe

    Returns:
        status (bool). Returns True if the key attribute was set successfully,
        else returns False


    """

    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    if not key in df.columns:
        logger.error('Input key ( %s ) not in the dataframe' % key)
        raise KeyError('Input key ( %s ) not in the dataframe' % key)

    if ch.is_key_attribute(df, key) is False:
        logger.warning(
            'Attribute (' + key + ') does not qualify to be a key; '
                                  'Not setting/replacing the key')
        return False
    else:
        return set_property(df, 'key', key)


# def gentle_set_key(df, key):
#     """
#     Set the key attribute for a dataframe
#
#     Args:
#         df (pandas dataframe): Dataframe for which the key must be set
#         key (str): Key attribute in the dataframe
#
#     Returns:
#         status (bool). Returns True if the key attribute was set successfully,
# else returns False
#
#     """
#
#     if not isinstance(df, pd.DataFrame):
#         logger.error('Input object is not of type pandas data frame')
#         raise AssertionError('Input object is not of type pandas data frame')
#
#     if not key in df.columns:
#         logger.warning('Input key ( %s ) not in the dataframe' %key)
#         return False
#
#     if ch.is_key_attribute(df, key) is False:
#         logger.warning('Attribute (' + key + ') does not qualify to be a key;
# Not setting/replacing the key')
#         return False
#     else:
#         return set_property(df, 'key', key)



def get_fk_ltable(df):
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    return get_property(df, 'fk_ltable')


def get_fk_rtable(df):
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    return get_property(df, 'fk_rtable')


def set_fk_ltable(df, fk_ltable):
    """
    Set foreign key attribute to the left table
    Args:
        df (pandas dataframe): Dataframe for which the foreign key must be set
        fk_ltable (str): Foreign key attribute in the dataframe

    Returns:
        status (bool). Returns True if the ltable foreign key attribute was set successfully, else returns False
    """
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    if not fk_ltable in df.columns:
        logger.error('Input attr. ( %s ) not in the dataframe' % fk_ltable)
        raise KeyError('Input attr. ( %s ) not in the dataframe' % fk_ltable)

    return set_property(df, 'fk_ltable', fk_ltable)


def validate_and_set_fk_ltable(df_foreign, fk_ltable, ltable, l_key):
    # validations are done inside the check_fk_constraint fn.
    status = ch.check_fk_constraint(df_foreign, fk_ltable, ltable, l_key)
    if status == True:
        return set_property(df_foreign, 'fk_ltable', fk_ltable)
    else:
        logger.warning(
            'FK constraint for ltable and fk_ltable is not satisfied; Not setting the '
            'fk_ltable and ltable')
        return False


def validate_and_set_fk_rtable(df_foreign, fk_rtable, rtable, r_key):
    # validations are done inside the check_fk_constraint fn.
    status = ch.check_fk_constraint(df_foreign, fk_rtable, rtable, r_key)
    if status == True:
        return set_property(df_foreign, 'fk_rtable', fk_rtable)
    else:
        logger.warning(
            'FK constraint for rtable and fk_rtable is not satisfied; Not setting the fk_rtable and rtable')
        return False


def set_fk_rtable(df, fk_rtable):
    """
    Set foreign key attribute to the right table
    Args:
        df (pandas dataframe): Dataframe for which the foreign key must be set
        fk_rtable (str): Foreign key attribute in the dataframe

    Returns:
        status (bool). Returns True if the rtable foreign key attribute was set successfully, else returns False
    """
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    if not fk_rtable in df.columns:
        logger.error('Input attr. ( %s ) not in the dataframe' % fk_rtable)
        raise KeyError('Input attr. ( %s ) not in the dataframe' % fk_rtable)

    return set_property(df, 'fk_rtable', fk_rtable)


def get_reqd_metadata_from_catalog(df, reqd_metadata):
    """
    Get a list of properties from the catalog

    Args:
        df (pandas dataframe): Dataframe for which the properties must be retrieved
        reqd_metadata (list): List of properties to be retrieved

    Returns:
        properties (dict)

    Notes:
        This is an internal helper function.


    """
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    if not isinstance(reqd_metadata, list):
        reqd_metadata = [reqd_metadata]

    metadata = {}
    d = get_all_properties(df)

    diff_elts = set(reqd_metadata).difference(d)
    if len(diff_elts) != 0:
        logger.error('All the required metadata is not present in the catalog')
        raise AssertionError(
            'All the required metadata is not present in the catalog')

    for m in reqd_metadata:
        if m in d:
            metadata[m] = d[m]
    return metadata


def _update_reqd_metadata_with_kwargs(metadata, kwargs_dict, reqd_metadata):
    """
    Update the metadata with input args

    Args:
        metadata (dict): Properties dictonary
        kwargs_dict (dict): Input key-value args
        reqd_metadata (list): List of properties to be updated.

    Returns:
        updated properties (dict)

    Notes:
        This is an internal helper function.


    """
    if not isinstance(metadata, dict):
        logger.error('Input metdata is not of type dict')
        raise AssertionError('Input metdata is not of type dict')

    if not isinstance(kwargs_dict, dict):
        logger.error('Input kwargs_dict is not of type dict')
        raise AssertionError('Input kwargs_dict is not of type dict')

    if not isinstance(reqd_metadata, list):
        reqd_metadata = [reqd_metadata]

    diff_elts = set(reqd_metadata).difference(kwargs_dict.keys())
    if len(diff_elts) != 0:
        logger.error('All the required metadata is not present in the catalog')
        raise AssertionError(
            'All the required metadata is not present in the catalog')

    for m in reqd_metadata:
        if m in kwargs_dict:
            metadata[m] = kwargs_dict[m]
    return metadata


def _get_diff_with_reqd_metadata(metadata, reqd_metadata):
    """
    Find what metadata is missing from the required list

    Args:
        metadata (dict): Property dictionary
        reqd_metadata (list): List of properties

    Returns:
        diff list (list) of properties between the property dictionary and the properties
        list

    Notes:
        This is an internal helper function
    """
    if not isinstance(metadata, dict):
        logger.error('Input metdata is not of type dict')
        raise AssertionError('Input metdata is not of type dict')

    k = metadata.keys()
    if not isinstance(reqd_metadata, list):
        reqd_metadata = [reqd_metadata]
    d = set(reqd_metadata).difference(k)
    return d


def is_all_reqd_metadata_present(metadata, reqd_metadata):
    """
    Check if all the required metadata are present

    Args:
        metadata (dict): Property dictionary
        reqd_metadata (list): List of properties

    Returns:
        result (bool). Returns True if all the required metadata is present, else returns False

    Notes:
        This is an internal helper function

    """
    if not isinstance(metadata, dict):
        logger.error('Input metdata is not of type dict')
        raise AssertionError('Input metdata is not of type dict')

    d = _get_diff_with_reqd_metadata(metadata, reqd_metadata)
    if len(d) == 0:
        return True
    else:
        return False


def show_properties(df):
    if not is_dfinfo_present(df):
        logger.error('Dataframe information is not present in the catalog')
        return
    metadata = get_all_properties(df)
    print('id: ' + str(id(df)))
    for prop, value in six.iteritems(metadata):
        if isinstance(value, six.string_types):
            print(prop + ": " + value)
        else:
            print(prop + "(obj.id): " + str(id(value)))


def show_properties_for_id(obj_id):
    catalog = Catalog.Instance()
    metadata = catalog.get_all_properties_for_id(obj_id)
    print('id: ' + str(obj_id))
    for prop, value in six.iteritems(metadata):
        if isinstance(value, six.string_types):
            print(prop + ": " + value)
        else:
            print(prop + "(obj.id): " + str(id(value)))


def set_candset_properties(candset, key, fk_ltable, fk_rtable, ltable, rtable):
    set_property(candset, 'key', key)
    set_fk_ltable(candset, fk_ltable)
    set_fk_rtable(candset, fk_rtable)
    set_property(candset, 'ltable', ltable)
    set_property(candset, 'rtable', rtable)


def validate_metadata_for_table(table, key, out_str, lgr, verbose):
    if not isinstance(table, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    if not key in table.columns:
        logger.error('Input key ( %s ) not in the dataframe' % key)
        raise KeyError('Input key ( %s ) not in the dataframe' % key)

    ch.log_info(lgr, 'Validating ' + out_str + ' key: ' + str(key), verbose)
    assert isinstance(key,
                      six.string_types) is True, 'Key attribute must be a string.'
    assert ch.check_attrs_present(table,
                                  key) is True, 'Key attribute is not present in the ' + out_str + ' table'
    assert ch.is_key_attribute(table, key, verbose) == True, 'Attribute ' + str(
        key) + \
                                                             ' in the ' + out_str + ' table ' \
                                                                                    'does not qualify to be the key'
    ch.log_info(lgr, '..... Done', verbose)
    return True


def validate_metadata_for_candset(candset, key, fk_ltable, fk_rtable, ltable,
                                  rtable,
                                  l_key, r_key,
                                  lgr, verbose):
    if not isinstance(candset, pd.DataFrame):
        logger.error('Input cand.set is not of type pandas data frame')
        raise AssertionError('Input cand.set is not of type pandas data frame')

    if not key in candset.columns:
        logger.error('Input key ( %s ) not in the dataframe' % key)
        raise KeyError('Input key ( %s ) not in the dataframe' % key)

    if not fk_ltable in candset.columns:
        logger.error('Input fk_ltable ( %s ) not in the dataframe' % fk_ltable)
        raise KeyError(
            'Input fk_ltable ( %s ) not in the dataframe' % fk_ltable)

    if not fk_rtable in candset.columns:
        logger.error('Input fk_rtable ( %s ) not in the dataframe' % fk_rtable)
        raise KeyError(
            'Input fk_rtable ( %s ) not in the dataframe' % fk_rtable)

    if not isinstance(ltable, pd.DataFrame):
        logger.error('Input ltable is not of type pandas data frame')
        raise AssertionError('Input ltable is not of type pandas data frame')

    if not isinstance(rtable, pd.DataFrame):
        logger.error('Input rtable is not of type pandas data frame')
        raise AssertionError('Input rtable is not of type pandas data frame')

    if not l_key in ltable:
        logger.error('ltable key ( %s ) not in ltable' % l_key)
        raise KeyError('ltable key ( %s ) not in ltable' % l_key)

    if not r_key in rtable:
        logger.error('rtable key ( %s ) not in rtable' % r_key)
        raise KeyError('rtable key ( %s ) not in rtable' % r_key)

    validate_metadata_for_table(candset, key, 'cand.set', lgr, verbose)

    ch.log_info(lgr, 'Validating foreign key constraint for left table',
                verbose)
    assert ch.check_fk_constraint(candset, fk_ltable, ltable,
                                  l_key) == True, 'Cand.set does not satisfy foreign key ' \
                                                  'constraint with the left table'
    ch.log_info(lgr, '..... Done', verbose)
    ch.log_info(lgr, 'Validating foreign key constraint for right table',
                verbose)
    assert ch.check_fk_constraint(candset, fk_rtable, rtable,
                                  r_key) == True, 'Cand.set does not satisfy foreign key ' \
                                                  'constraint with the right table'
    ch.log_info(lgr, '..... Done', verbose)

    return True


def get_keys_for_ltable_rtable(ltable, rtable, lgr, verbose):
    if not isinstance(ltable, pd.DataFrame):
        logger.error('Input ltable is not of type pandas data frame')
        raise AssertionError('Input ltable is not of type pandas data frame')

    if not isinstance(rtable, pd.DataFrame):
        logger.error('Input rtable is not of type pandas data frame')
        raise AssertionError('Input rtable is not of type pandas data frame')

    ch.log_info(lgr, 'Required metadata: ltable key, rtable key', verbose)
    ch.log_info(lgr, 'Getting metadata from the catalog', verbose)
    l_key = get_key(ltable)
    r_key = get_key(rtable)
    ch.log_info(lgr, '..... Done', verbose)
    return l_key, r_key


def get_metadata_for_candset(candset, lgr, verbose):
    if not isinstance(candset, pd.DataFrame):
        logger.error('Input candset is not of type pandas data frame')
        raise AssertionError('Input candset is not of type pandas data frame')

    ch.log_info(lgr, 'Getting metadata from the catalog', verbose)
    key = get_key(candset)
    fk_ltable = get_fk_ltable(candset)
    fk_rtable = get_fk_rtable(candset)
    ltable = get_ltable(candset)
    rtable = get_rtable(candset)
    l_key = get_key(ltable)
    r_key = get_key(rtable)
    ch.log_info(lgr, '..... Done', verbose)
    return key, fk_ltable, fk_rtable, ltable, rtable, l_key, r_key


def get_ltable(candset):
    return get_property(candset, 'ltable')


def get_rtable(candset):
    return get_property(candset, 'rtable')
