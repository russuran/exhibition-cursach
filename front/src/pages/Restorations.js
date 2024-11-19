import React, { useEffect, useState } from 'react';
import { Table, Button, Modal } from 'antd';
import axios from 'axios';
import RestorationForm from '../components/RestorationForm';

const Restorations = () => {
    const [restorations, setRestorations] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentRestoration, setCurrentRestoration] = useState(null);

    useEffect(() => {
        fetchRestorations();
    }, []);

    const fetchRestorations = async () => {
        const response = await axios.get('http://localhost:3001/restorations/');
        setRestorations(response.data);
    };

    const handleDelete = async (restorationId) => {
        await axios.delete(`http://localhost:3001/restorations/${restorationId}`);
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
            await axios.put(`http://localhost:3001/restorations/${currentRestoration.restoration_id}`, values);
        } else {
            await axios.post('http://localhost:3001/restorations/', values);
        }
        fetchRestorations();
        handleModalClose();
    };

    return (
        <div>
            <Button type="primary" onClick={() => handleModalOpen(null)} style={{ marginBottom: 16 }}>
                Добавить реставрацию
            </Button>
            <Table dataSource={restorations} rowKey="restoration_id">
                <Table.Column title="Код Экспоната" dataIndex="exhibit_id" />
                <Table.Column title="Код Сотрудника" dataIndex="employee_id" />
                <Table.Column title="Дата Начала" dataIndex="start_date" />
                <Table.Column title="Дата Конца" dataIndex="end_date" />
                <Table.Column title="Actions" render={(text, restoration) => (
                    <>
                        <Button onClick={() => handleModalOpen(restoration)}>Редактировать</Button>
                        <Button onClick={() => handleDelete(restoration.restoration_id)}>Удалить</Button>
                    </>
                )} />
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
