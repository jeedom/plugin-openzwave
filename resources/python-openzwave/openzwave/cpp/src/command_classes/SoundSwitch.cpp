//-----------------------------------------------------------------------------
//
//	Color.cpp
//
//	Implementation of the Z-Wave COMMAND_CLASS_COLOR
//
//	Copyright (c) 2014 GizMoCuz
//
//	SOFTWARE NOTICE AND LICENSE
//
//	This file is part of OpenZWave.
//
//	OpenZWave is free software: you can redistribute it and/or modify
//	it under the terms of the GNU Lesser General Public License as published
//	by the Free Software Foundation, either version 3 of the License,
//	or (at your option) any later version.
//
//	OpenZWave is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//	GNU Lesser General Public License for more details.
//
//	You should have received a copy of the GNU Lesser General Public License
//	along with OpenZWave.  If not, see <http://www.gnu.org/licenses/>.
//
//-----------------------------------------------------------------------------

#include <iostream>
#include <iomanip>


#include "command_classes/CommandClasses.h"
#include "command_classes/SoundSwitch.h"
#include "Defs.h"
#include "Msg.h"
#include "Node.h"
#include "Driver.h"
#include "platform/Log.h"

#include "value_classes/ValueInt.h"
#include "value_classes/ValueString.h"
#include "value_classes/ValueByte.h"

#include "tinyxml.h"


using namespace OpenZWave;

enum SoundSwitchCmd
{
	SoundSwitch_ToneNum_Get = 0x01,
	SoundSwitch_ToneNum_Report = 0x02,
	SoundSwitch_ToneInfo_Get = 0x03,
	SoundSwitch_ToneInfo_Report = 0x04,
	SoundSwitch_Config_Set = 0x05,
	SoundSwitch_Config_Get = 0x06,
	SoundSwitch_Config_Report = 0x07,
	SoundSwitch_Play_Set = 0x08,
	SoundSwitch_Play_Get = 0x09,
	SoundSwitch_Play_Report = 0x0A
};

enum SoundSwitch_ValueID_Index
{
    SoundSwitch_ToneCount                         = 0x00,
    SoundSwitch_Tones                             = 0x01,
    SoundSwitch_Volume                            = 0x02,
    SoundSwitch_Default_Tone                      = 0x03,
    SoundSwitch_PlaySound                         = 0x08

};
//-----------------------------------------------------------------------------
// <SoundSwitch::SoundSwitch>
// Constructor
//-----------------------------------------------------------------------------
SoundSwitch::SoundSwitch
(
		uint32 const _homeId,
		uint8 const _nodeId
):
CommandClass( _homeId, _nodeId ),
m_toneCount(0)
{
    SetStaticRequest( StaticRequest_Values );
	Log::Write(LogLevel_Info, GetNodeId(), "SoundSwitch - Created %d", HasStaticRequest( StaticRequest_Values ));
}



//-----------------------------------------------------------------------------
// <SoundSwitch::RequestState>
// Request current state from the device
//-----------------------------------------------------------------------------
bool SoundSwitch::RequestState(uint32 const _requestFlags, uint8 const _instance, Driver::MsgQueue const _queue)
			{
				bool requests = false;
				if ((_requestFlags & RequestFlag_Static) && HasStaticRequest(StaticRequest_Values))
				{
					requests |= RequestValue(_requestFlags, SoundSwitch_ToneCount, _instance, _queue);
				}
				if (_requestFlags & RequestFlag_Dynamic) 
				{
					requests |= RequestValue(_requestFlags, SoundSwitch_Volume, _instance, _queue);
				}

				return requests;
			}

//-----------------------------------------------------------------------------
// <SoundSwitch::RequestValue>
// Request current value from the device
//-----------------------------------------------------------------------------
bool SoundSwitch::RequestValue
(
		uint32 const _requestFlags,
		uint8 const _index,
		uint8 const _instance,
		Driver::MsgQueue const _queue
)
{
	if (_index == SoundSwitch_ToneCount) {
		Msg* msg = new Msg( "SoundSwitch_ToneNum_Get", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId() );
		msg->SetInstance( this, _instance );
		msg->Append( GetNodeId() );
		msg->Append( 2 );
		msg->Append( GetCommandClassId() );
		msg->Append( SoundSwitch_ToneNum_Get );
		msg->Append( GetDriver()->GetTransmitOptions() );
		GetDriver()->SendMsg( msg, _queue );
		return true;
	}else if (_index == SoundSwitch_Volume || _index == SoundSwitch_Default_Tone) {
			Msg* msg = new Msg("SoundSwitchCmd_Tones_Config_Get", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId());
			msg->SetInstance(this, _instance);
			msg->Append(GetNodeId());
			msg->Append(2);
			msg->Append(GetCommandClassId());
			msg->Append(SoundSwitch_Config_Get);
			msg->Append(GetDriver()->GetTransmitOptions());
			GetDriver()->SendMsg(msg, Driver::MsgQueue_Send);
			return true;
	}
	return false;
}
//-----------------------------------------------------------------------------
// <SoundSwitch::ReadXML>
// Class specific configuration
//-----------------------------------------------------------------------------
void SoundSwitch::ReadXML
(
		TiXmlElement const* _ccElement
)
{
	int32 intVal;

	CommandClass::ReadXML( _ccElement );
	if( TIXML_SUCCESS == _ccElement->QueryIntAttribute( "toneCount", &intVal ) )
	{
		m_toneCount = intVal;
	}
}

//-----------------------------------------------------------------------------
// <SoundSwitch::WriteXML>
// Class specific configuration
//-----------------------------------------------------------------------------
void SoundSwitch::WriteXML
(
		TiXmlElement* _ccElement
)
{
	char str[32];

	CommandClass::WriteXML( _ccElement );
	snprintf( str, sizeof(str), "%d", m_toneCount );
	_ccElement->SetAttribute( "toneCount", str);
}


//-----------------------------------------------------------------------------
// <SoundSwitch::HandleMsg>
// Handle a message from the Z-Wave network
//-----------------------------------------------------------------------------
bool SoundSwitch::HandleMsg
(
		uint8 const* _data,
		uint32 const _length,
		uint32 const _instance	// = 1
)
{
	if (SoundSwitch_ToneNum_Report == (SoundSwitchCmd)_data[0])
	{
		int toneCount = _data[1];
		if (m_toneCount == 0)
		{
			m_toneCount = toneCount;
		}
		if ( ValueInt* value = static_cast<ValueInt*>( GetValue( _instance, SoundSwitch_ToneCount)))
		{
			value->OnValueRefreshed(m_toneCount);
			value->Release();
		} else {
			Log::Write( LogLevel_Warning, GetNodeId(), "Can't find ValueID for ToneCount");
		}
		return true;
	} if (SoundSwitch_ToneInfo_Report == (SoundSwitchCmd) _data[0])
		{
			uint8 index = _data[1];
			uint16 duration = (_data[2] << 8) + _data[3];
			string name((const char *) &_data[5], _data[4]);
			m_toneInfo[index].duration = duration;
			m_toneInfo[index].name = name;
			Log::Write(LogLevel_Info, GetNodeId(), "Received SoundSwitch Tone Info Report: %d - %s - %d sec", index, name.c_str(), duration);
			if (index == m_toneCount)
			{
				vector<ValueList::Item> items;
				{
					ValueList::Item item;
					item.m_label = "Inactive";
					item.m_value = 0;
					items.push_back(item);
				}
				for (unsigned int i = 1; i <= m_toneCount; i++)
				{
					ValueList::Item item;
					char str[268]; // name is max 255, duration can be max 65535 so this should be enough space
					snprintf(str, sizeof(str), "%s (%d sec)", m_toneInfo[i].name.c_str(), m_toneInfo[i].duration);
					item.m_label = str;
					item.m_value = i;
					items.push_back(item);
				}
				{
					ValueList::Item item;
					item.m_label = "Default Tone";
					item.m_value = 0xff;
					items.push_back(item);
				}
				if (Node* node = GetNodeUnsafe())
				{
					node->CreateValueList(ValueID::ValueGenre_User, GetCommandClassId(), _instance,  SoundSwitch_Tones, "Tones", "", false, false, m_toneCount, items, 0, 0);
					node->CreateValueList(ValueID::ValueGenre_Config, GetCommandClassId(), _instance, SoundSwitch_Default_Tone, "Default Tone", "", false, false, m_toneCount, items, 0, 0);
				}
				/* after we got the list of Tones, Get the Configuration */
				Msg* msg = new Msg("SoundSwitchCmd_Tones_Config_Get", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId());
				msg->SetInstance(this, _instance);
				msg->Append(GetNodeId());
				msg->Append(2);
				msg->Append(GetCommandClassId());
				msg->Append(SoundSwitch_Config_Get);
				msg->Append(GetDriver()->GetTransmitOptions());
				GetDriver()->SendMsg(msg, Driver::MsgQueue_Send);
			}
			return true;
		}
		if (SoundSwitch_Config_Report == (SoundSwitchCmd) _data[0])
				{
					uint8 volume = _data[1];
					uint8 defaulttone = _data[2];
					if (volume > 100)
						volume = 100;
					Log::Write(LogLevel_Info, GetNodeId(), "Received SoundSwitch Tone Config report - Volume: %d, defaulttone: %d", volume, defaulttone);
					if (ValueByte* value = static_cast<ValueByte*>(GetValue(_instance, SoundSwitch_Volume)))
					{
						value->OnValueRefreshed(volume);
						value->Release();
					}
					if (ValueList* value = static_cast<ValueList*>(GetValue(_instance, SoundSwitch_Default_Tone)))
					{
						value->OnValueRefreshed(defaulttone);
						value->Release();
					}
					ClearStaticRequest(StaticRequest_Values);
					return true;
				}
				if (SoundSwitch_Play_Report == (SoundSwitchCmd) _data[0])
				{
					Log::Write(LogLevel_Info, GetNodeId(), "Received SoundSwitch Tone Play report: %d", _data[1]);
					if (ValueList* value = static_cast<ValueList*>(GetValue(_instance, SoundSwitch_Tones)))
					{
						value->OnValueRefreshed(_data[1]);
						value->Release();
					}
					return true;
				}
	return false;
}

//-----------------------------------------------------------------------------
// <SoundSwitch::SetValue>
// Set a new value for the sound
//-----------------------------------------------------------------------------
bool SoundSwitch::SetValue
(
	Value const& _value
)
{
	uint8 instance = _value.GetID().GetInstance();

	switch( _value.GetID().GetIndex() )
	{
		case SoundSwitch_Play_Set:
		{
			ValueByte const* value = static_cast<ValueByte const*>(&_value);
			ValueByte* valueObj = static_cast<ValueByte*>( GetValue( instance, SoundSwitch_Play_Set ) );
			Log::Write( LogLevel_Info, GetNodeId(), "Play sound::Set - Setting node %d to %d", GetNodeId(), value->GetValue());
			Msg* msg = new Msg( "SoundPlay_Set", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true );
			msg->SetInstance( this, instance );
			msg->Append( GetNodeId() );
			msg->Append( 3 );
			msg->Append( GetCommandClassId() );
			msg->Append( SoundSwitch_Play_Set );
			msg->Append( value->GetValue() );
			msg->Append( GetDriver()->GetTransmitOptions() );
			GetDriver()->SendMsg( msg, Driver::MsgQueue_Send );
			valueObj->OnValueRefreshed(value->GetValue());
			valueObj->Release();
			return true;
			break;
		}
		case SoundSwitch_Volume:
		{
			uint8 volume = 0xff;
			if (ValueByte const* value = static_cast<ValueByte const*>(&_value))
			{
				volume = value->GetValue();
				if (volume > 100) {
					volume = 0xFF;
				}
			}
			Msg* msg = new Msg("SoundSwitch_Config_Set", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true);
			msg->SetInstance(this, instance);
			msg->Append(GetNodeId());
			msg->Append(4);
			msg->Append(GetCommandClassId());
			msg->Append(SoundSwitch_Config_Set);
			msg->Append(volume);
			msg->Append(0);
			msg->Append(GetDriver()->GetTransmitOptions());
			GetDriver()->SendMsg(msg, Driver::MsgQueue_Send);
			return true;
			break;
		}
		case SoundSwitch_Default_Tone:
		{
			uint8 defaulttone = 0x00;
			if (ValueList const* value = static_cast<ValueList const*>(&_value))
			{
				ValueList::Item const *item = value->GetItem();
				if (item == NULL)
					return false;
				defaulttone = item->m_value;
				/* 0 means dont update the Default Tone 0xFF is the Default tone! */
				if (defaulttone == 0xFF)
					defaulttone = 1;
			}
			Msg* msg = new Msg("SoundSwitch_Config_Set", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true);
			msg->SetInstance(this, instance);
			msg->Append(GetNodeId());
			msg->Append(4);
			msg->Append(GetCommandClassId());
			msg->Append(SoundSwitch_Config_Set);
			msg->Append(0xFF);
			msg->Append(defaulttone);
			msg->Append(GetDriver()->GetTransmitOptions());
			GetDriver()->SendMsg(msg, Driver::MsgQueue_Send);
			return true;
			break;
		}
	}
	return false;
}

//-----------------------------------------------------------------------------
// <SoundSwitch::CreateVars>
// Create the values managed by this command class
//-----------------------------------------------------------------------------
void SoundSwitch::CreateVars
(
		uint8 const _instance
)
{
	if( Node* node = GetNodeUnsafe() )
	{
		node->CreateValueInt( ValueID::ValueGenre_Config, GetCommandClassId(), _instance, SoundSwitch_ToneCount, "Tone Count", "", true, false, 0, 0 );
		node->CreateValueByte( ValueID::ValueGenre_User, GetCommandClassId(), _instance, SoundSwitch_PlaySound, "Play Tone", "", false, false, 0, 0 );
		node->CreateValueByte(ValueID::ValueGenre_User, GetCommandClassId(), _instance, SoundSwitch_Volume, "Volume", "", false, false, 100, 0);
	}
}