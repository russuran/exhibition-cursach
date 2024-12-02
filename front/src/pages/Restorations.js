import React, { useEffect, useState } from 'react';
import { Table, Button, Modal } from 'antd';
import axios from 'axios';
import RestorationForm from '../components/RestorationForm';

const Restorations = () => {
    const [restorations, setRestorations] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentRestoration, setCurrentRestoration] = useState(null);

    const role = localStorage.getItem('role');

    useEffect(() => {
        fetchRestorations();
    }, []);

    const fetchRestorations = async () => {
        const response = await axios.get('http://localhost:5000/restorations/');
        setRestorations(response.data);
    };

    const handleDelete = async (restorationId) => {
        await axios.delete(`http://localhost:5000/restorations/${restorationId}`);
        fetchRestorations();
    };

    const handleModalOpen = (restoration) => {
        setCurrentRestoration(restoration);
        setIsModalVisible(true);
    };

    const handleModalClose = () => {
        setCurrentRestoration(null);
        setIsModalVisible(false);
    };

    const handleFormSubmit = async (values) => {
        if (currentRestoration) {
            await axios.put(`http://localhost:5000/restorations/${currentRestoration.restoration_id}`, values);
        } else {
            await axios.post('http://localhost:5000/restorations/', values);
        }
        fetchRestorations();
        handleModalClose();
    };

    return (
        <div>
            {role === 'personal' && (
                <Button type="primary" onClick={() => handleModalOpen(null)} style={{ marginBottom: 16 }}>
                    Добавить Реставрацию
                </Button>
            )}
            <Table dataSource={restorations} rowKey="restoration_id">
                <Table.Column title="Код Экспоната" dataIndex="exhibit_id" />
                <Table.Column title="Код Сотрудника" dataIndex="employee_id" />
                <Table.Column title="Причина Реставрации" dataIndex="restoration_reason" />
                <Table.Column title="Дата Начала" dataIndex="start_date" />
                <Table.Column title="Дата Конца" dataIndex="end_date" />
                {role === 'personal' && 
                <Table.Column title="Действия" render={(text, restoration) => (
                    <div style={{ display: 'flex', gap: 10 }}>
                        <Button onClick={() => handleModalOpen(restoration)}>Редактировать</Button>
                        <Button onClick={() => handleDelete(restoration.restoration_id)}>Удалить</Button>
                    </div>
                )} />
                }
            </Table>
            <Modal
                title={currentRestoration ? "Редактировать реставрацию" : "Добавить реставрацию"}
                visible={isModalVisible}
                onCancel={handleModalClose}
                footer={null}
            >
                <RestorationForm
                    initialValues={currentRestoration}
                    onSubmit={handleFormSubmit}
                />
            </Modal>
        </div>
    );
};

export default Restorations;
